#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Refine EITI dataset

import unicodecsv

FILE_EITI = "output/Country-level.csv"
FILE_DATA = "../data/eiti.csv"
FILE_TOTAL = "../data/eiti_total.csv"

H_DATA = ['Report ID', 'Years Covered', 'Country Name', 'Lookup',
'Region', 'Sector', 'Mining', 'Gas', 'Oil', 'Commodity',
'Total Production Volume (external source)', 
'Total Reconciled Production Volume (from EITI Report)', 
'Total Production Volume (from EITI Report, government source)', 
'Total Production Volume (from EITI Report, companies source)', 
'Volume Metric', 'Price', 'Per Unit', 
'Source for Total Production Volume & Price Information', 
'Total Production Value (US$)', 'Revenue Streams Covered', 
'Includes In-kind Payments', 'Added to Payments by Author', 
'Payments Received by Government from Covered Companies (US$)', 
'Payments Made by Covered Companies (US$)', 
'Proportion of Total Revenue/Production Covered (as indicated in EITI Report)', 
'Total Government Extractives Revenue (US$)', 
'Source for Total Government Extractives Revenues', "Government's share", 
'Currency', 'Exchange Rate Utilized, US$1:LC', 'Disaggregation', 
'In-kind Payment Volumes', 'In-kind Payment Value (US$)', 
'Nature of Subsidy', 'Amount of Subsidy (US$)', 
'Number of Companies Requested to Report', 'Companies Requested to Report', 
'Number of Reporting Companies', 'Publication Date', 'Updated Date', 
'Name of the Reconciler', 'EITI Report', 'Page of the Report', 'Comments']

H_TOTAL = ['Report ID', 'Years Covered', "Country Name", "Lookup", "Region",
"Country Webpage", "Sector", "Total Production Value (US$)", 
"Revenue Streams Covered", "Includes In-kind Payments", 
"Added to Payments by Author", 
"Payments Received by Government from Covered Companies (US$)",
"Payments Made by Covered Companies (US$)",
'Proportion of Total Revenue/Production Covered (as indicated in EITI Report)', 
'Total Government Extractives Revenue (US$)', 
'Source for Total Government Extractives Revenues', "Government's share", 
'Currency', 'Exchange Rate Utilized, US$1:LC', 'Disaggregation', 
'In-kind Payment Volumes', 'In-kind Payment Value (US$)', 
'Nature of Subsidy', 'Amount of Subsidy (US$)', 
'Number of Companies Requested to Report', 'Companies Requested to Report', 
'Number of Reporting Companies', 'Publication Date', 'Updated Date', 
'Name of the Reconciler', 'EITI Report', 'Page of the Report', 'Comments']

def make_row(csv_file, row, headers):
    for k, v in row.items():     
        if k not in headers: row.pop(k)
    csv_file.writerow(row)

def parse_eiti(filename):
    with open(filename, "r") as f_eiti:
        csvf = unicodecsv.DictReader(f_eiti)
        f_data = open(FILE_DATA, "wb")
        f_total = open(FILE_TOTAL, "wb")
        
        # Create CSV files for disaggregated row data and total data
        csv_data = unicodecsv.DictWriter(f_data, fieldnames=H_DATA)
        csv_total = unicodecsv.DictWriter(f_total, fieldnames=H_TOTAL)
        
        # Write header rows
        csv_data.writeheader()
        csv_total.writeheader()
        
        seen_report_ID = ""
        
        known_data = []
        
        for i, row in enumerate(csvf):
            if row["Report ID"] != seen_report_ID:
                # Process total row
                make_row(csv_total, row, H_TOTAL)
                seen_report_ID = row["Report ID"]
            else:
                if row["Total line?"] == "Total": continue
                known_data.append((i, row))
                
    kd = dict(known_data)
    
    # Roll up o/w rows
    ow = False
    ow_prod_vol = []
    ow_prod_vol_metric = []
    ow_source = []
    prod_vol_col = "Total Production Volume (external source)"
    prod_vol_metric_col = "Volume Metric"
    source_col = 'Source for Total Production Volume & Price Information'
    for i, d in sorted(kd.items(), reverse=True):
        if d['Commodity'].startswith(("  o/w", "o/w")):
            # If row starts with o/w then roll up prod vol and get source
            ow = True
            if d[prod_vol_col] != "":
                ow_prod_vol.append(float(d[prod_vol_col]))
            if d[source_col] != "":
                ow_source.append(d[source_col])
            if d[prod_vol_metric_col] != "":
                ow_prod_vol_metric.append(d[prod_vol_metric_col])
            # Delete this row
            kd.pop(i)
            continue
        if ow:
            d[prod_vol_col] = sum(ow_prod_vol)
            d[prod_vol_metric_col] = "; ".join(set(ow_prod_vol_metric))
            d[source_col] = "%s; %s" % (d[source_col], 
                                          "; ".join(set(ow_source)))
            ow = False
            ow_prod_vol = []
            ow_prod_vol_metric = []
            ow_source = []
            
    for i, d in kd.items():
        make_row(csv_data, d, H_DATA)

if __name__ == '__main__':
    parse_eiti(FILE_EITI)