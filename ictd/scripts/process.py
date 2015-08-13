
import os
import requests
import logging
from pyexcel_ods import get_data
import json
import csv
import pycountry
import shutil
import time
# import pprint

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

source_url = 'http://www.ictd.ac/dataset/ICTDGRD_August2014_CentralGeneralMergedFull.ods'

start_time = time.time()

# Alt at
# http://www.ictd.ac/dataset/ICTD_Stata_files.zip

def download():
    """
	Downloads ICTD government revenue database from website and stores in cache for
    transformation process.
    """
    if not os.path.exists(args.filepath + '/cache'):
		os.makedirs(args.filepath + '/cache')
    if not os.path.exists(args.filepath + '/data'):
        os.makedirs(args.filepath + '/data')

    if not os.path.exists(local_filename):
        logger.info('Retrieving source data from %s ...' % source_url)
        r = requests.get(args.source_url, stream=True)

        with open(local_filename, 'wb') as fp:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    fp.write(chunk)
                    fp.flush()
        elapsed_time = time.time() - start_time
        logger.info('Retrieved source data from %s (elapsed time - %s seconds)' % (source_url, elapsed_time))
    else:
       logger.info('File exists, extracting json')

    # sheet_names = ['Central', 'General', 'Merged', 'Classifier', 'Var List']
    sheet_names = ['Central', 'General', 'Merged', 'Var List']
    extracted = False
    for sheet in sheet_names:
        dname = sheet.replace(' ', '_').lower()
        if os.path.exists(args.filepath + '/cache/' + dname + '.json'):
            extracted = True
    if extracted == False:
        in_data = get_data(local_filename)
        # sheet_names = in_data.keys()

        for sheet in sheet_names:
            d = in_data[sheet]
            dname = sheet.replace(' ', '_').lower()
            if not os.path.exists(args.filepath + '/cache/' + dname + '.json'):
                with open(args.filepath + '/cache/' + dname + '.json', 'wb') as outfile:
                    json.dump(d, outfile)
            else:
                logger.info('File exists, moving on')
    else:
        logger.info('All files exists, moving on')
    elapsed_time = time.time() - start_time
    logger.info('Source data downloaded to: %s (elapsed time - %d seconds)' % (local_filename, elapsed_time))


def transform():
    """
    Transforme cached ICTD database into datapackage for loading into ckan. Source is ODS 
    and export is flat csv files.
    """
    logger.info('Starting transfromation process of data from: %s' % local_filename)

    data_file_array = ['central', 'general', 'merged']
    # ['classifier', 'var_ist']

    in_data = {'headers': {}}
    out_data = {
        'central': [],
        'general': [],
        'merged': [],
        # 'classifier': [],
        'var_list': []
    }
    for f in data_file_array:
        with open(args.filepath + '/cache/' + f + '.json') as json_source:
            in_data[f] = json.load(json_source)
            in_data['headers'][f] = in_data[f][0]
    # with open(args.filepath + '/cache/classifier.json') as classifier:
    #     in_data['classifier'] = json.load(classifier)
    #     in_data['headers']['classifier'] = in_data['classifier'][1]
    with open(args.filepath + '/cache/var_list.json') as var_list:
        in_data['var_list'] = json.load(var_list)
        in_data['headers']['var_list'] = in_data['var_list'][1]

    #### MAIN DATASETS
    var_list = [
        'ISO',
        'Calendar year (nearest)',
        'Source',
        'Problem 1: Data Not Credible',
        'Problem 3: Data is of Questionable Analytical Comparability',
        'Revenue including social contributions',
        'Revenue excluding social contributions',
        'Revenue excluding Grants (including social contributions)',
        'Revenue excluding grants and social contributions',
        'Total Resource Revenue',
        'Resource taxes',
        'Resource Component of Taxes on income, profits, and capital gains',
        'Resource Component of Indirect',
        'Resources Component of Non-Tax'
    ]
    data_header = [
        'iso2c',
        'year',
        'source',
        'not_credible',
        'not_comparable',
        'rev_inc_soc_contr',
        'rev_ex_soc_contr',
        'rev_ex_grants_inc_soc_contr',
        'rev_ex_grants_ex_soc_contr',
        'tot_resource_rev',
        'resource_taxes',
        'resource_comp_tax_income',
        'resource_comp_indirect',
        'resourc_comp_non_tax'
    ]

    lkey = {'central': {}, 'general': {}, 'merged': {}}

    central_lkey = {}
    general_lkey = {}
    merged_lkey = {}

    for l in var_list:
        if l == 'Source':
            # no column title
            lkey['central'][l] = 3
            lkey['general'][l] = in_data['headers']['general'].index(l)
            lkey['merged'][l] = in_data['headers']['merged'].index(l)
        elif l == 'Revenue excluding Grants (including social contributions)':
            # lower case grants
            lkey['central'][l] = in_data['headers']['central'].index('Revenue excluding grants (including social contributions)')
            lkey['general'][l] = in_data['headers']['general'].index(l)
            lkey['merged'][l] = in_data['headers']['merged'].index(l)
        elif l == 'Calendar year (nearest)':
            # missing ' (nearest)'
            lkey['central'][l] = in_data['headers']['central'].index(l)
            lkey['general'][l] = in_data['headers']['general'].index('Calendar year')
            lkey['merged'][l] = in_data['headers']['merged'].index(l)
        else:
            lkey['central'][l] = in_data['headers']['central'].index(l)
            lkey['general'][l] = in_data['headers']['general'].index(l)
            lkey['merged'][l] = in_data['headers']['merged'].index(l)

    # iterate throug datafiles
    for df in data_file_array:
        # iterate through rows
        for row in range(1, len(in_data[df])):
            add_array = []
            iso3 = in_data[df][row][lkey[df]['ISO']]
            if iso3 != '':
                year = int(in_data[df][row][lkey[df]['Calendar year (nearest)']])
                # print year
            
                for var in var_list:
                    if var == 'ISO':
                        if iso3 == 'ANT':
                            iso2 = 'AN'
                        elif iso3 == 'KSV':
                            iso2 = 'XK'
                        elif iso3 == 'ROM':
                            iso2 = pycountry.countries.get(alpha3='ROU').alpha2
                        elif iso3 == 'TMP':
                            iso2 = pycountry.countries.get(alpha3='TLS').alpha2
                        elif iso3 == 'WBG':
                            iso2 = pycountry.countries.get(alpha3='PSE').alpha2
                        elif iso3 == 'ZAR':
                            iso2 = pycountry.countries.get(alpha3='COD').alpha2
                        elif iso3 == 'ADO':
                            iso2 = pycountry.countries.get(alpha3='AND').alpha2
                        elif iso3 == 'CHI':
                            iso2 = 'XC'
                        elif iso3 != '':
                            iso2 = pycountry.countries.get(alpha3=iso3).alpha2
                        else:
                            pass
                        add_array.append(iso2)
                    elif var == 'Calendar year (nearest)':
                        add_array.append(year)
                    elif var == 'Problem 1: Data Not Credible' or var == 'Problem 3: Data is of Questionable Analytical Comparability':
                        val = in_data[df][row][lkey[df][var]]
                        if val == 1:
                            add_array.append(True)
                        else:
                            add_array.append(False)
                    elif var == 'Source':
                        val = in_data[df][row][lkey[df][var]]
                        if val == 0 or val == '':
                            add_array.append('NULL')
                        else:
                            add_array.append(val.replace(',', ''))
                    else:
                        val = in_data[df][row][lkey[df][var]]
                        if val != '':
                            add_array.append(val)
                        else:
                            add_array.append('NULL')
                
                out_data[df].append(add_array)
        logger.info('Writing ' + df + '.csv file to data/ directory')
        write_csv(data_header, out_data[df], df)
        elapsed_time = time.time() - start_time
        logger.info('Finished writing %s.csv file to data/ directory (elapsed time - %d seconds)' % (df, elapsed_time))


    # #### CLASSIFIER - DOESNT SEEM NECESSARY
    # print in_data['classifier'][1]
    # print in_data['classifier'][2]
    # # for row in range(1,len(in_data['classifier'])):
    # #     print row
    

    #### VAR_LIST
    var_list_header = in_data['var_list'][1]
    for h in var_list_header:
        h = h.lower()
    var_list_array = []

    for row in range(2, len(in_data['var_list'])):
        if in_data['var_list'][row][0] == '' and in_data['var_list'][row][1] == '':
            pass
        else:
            var_list_array.append([in_data['var_list'][row][0].encode('utf-8').replace(',', ''), in_data['var_list'][row][1].encode('utf-8').replace(',', '')])

    write_csv(var_list_header, var_list_array, 'var_list')
    elapsed_time = time.time() - start_time
    logger.info('Finished writing var_list.csv file to data/ directory (elapsed time - %d seconds)' % elapsed_time)
    logger.info('Completed data transformation to data/ directory')

def write_csv(header, rows, filename):
    """
    Write rows to a CSV file. Use default dialect for the CSV. If a file name
    is not provided, the rows will be printed to standard output
    """

    # Set the file as stdout if no filename, else open the file for writing
    with open(args.filepath + '/data/' + filename + '.csv', 'wb') as output:
        # Create the csv writer
        csvwriter = csv.writer(output)
        # Write the header
        csvwriter.writerow(header)
        # Write all the rows
        csvwriter.writerows(rows)
        # Close the output file (or stdout)
        output.close()
    

def cleanup():
    shutil.rmtree(args.filepath + '/cache')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import argparse
    parser = argparse.ArgumentParser(
    	description='Process ICTD Gov Revenue data set')

    # Output file option
    parser.add_argument('-o', '--output', dest='filepath', action='store',
    	default=None, metavar='filepath',
    	help='define output filepath')

    # Source file option (default is the global source_url)
    parser.add_argument('-s', '--source', dest='source_url', action='store',
    	default=source_url, metavar='source_url',
    	help='source file to generate output from')

    # Parse the arguments into args
    args = parser.parse_args()

    local_filename = args.filepath + '/cache/' + args.source_url.split('/')[-1]

    download()
    transform()
    cleanup()
    elapsed_time = time.time() - start_time
    logger.info('ETL process complete: elapsed time - %d seconds' % elapsed_time)
