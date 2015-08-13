Resource Wealth and dependence data. Data is sourced from [the International Centre for Tax and Development](http://www.ictd.ac).

## Data
[The ICTD Government Revenue Dataset page](http://www.ictd.ac/en/about-ictd-government-revenue-dataset#Dataset)

###Structure
Main data comes in three sheets or tables: central, general and merged (see notes for description). Each is organized into country-year records with multiple variables. Included is a field dictionary for the entire dataset: var_list.

###Included variables

* **iso2c** - [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country ID *(string)*
* **year** - Year *(int)*
* **source** - Source *(string)*
* **not_credible** - Problem 1: Data Not Credible *(bool)*
* **not_comparable** -  Problem 3: Data is of Questionable Analytical Comparability *(bool)*
* **rev_inc_soc_contr** - Revenue including social contributions *(float)*
* **rev_ex_soc_contr** - Revenue excluding social contributions *(float)*
* **rev_ex_grants_inc_soc_contr** - Revenue excluding Grants (including social contributions) *(float)*
* **rev_ex_grants_ex_soc_contr** - Revenue excluding grants and social contributions *(float)*
* **tot_resource_rev** - Total Resource Revenue *(float)*
* **resource_taxes** - Resource taxes *(float)*
* **resource_comp_tax_income** - Resource Component of Taxes on income, profits, and capital gains *(float)*
* **resource_comp_indirect** - Resource Component of Indirect *(float)*
* **resourc_comp_non_tax** - Resources Component of Non-Tax *(float)*
        
### Notes from the Source
Contains individual data sheets with the Central and General government data reported as % of GDP, as described in the [Working Paper](http://www.ictd.ac/sites/default/files/ICTD%20WP19.pdf).  This is followed by the sheet "merged", which combines central and general government data into a single dataset, also as described in the Working Paper.  The "Classifier" (*Not included in datapackage-eds*) datasheet allows you to alter whether the final dataset draws on central or general government data for any given country, though we would not recommend making changes, and this is largely included for transparency about whether data is central or general for any given country.


## License

The maintainers have licensed under the [Creative Commons Attribution 4.0 (CC-BY-4.0) license](http://opendefinition.org/licenses/cc-by). The data source at ICTD indicates no obvious restrictions on data usage. This means that database rights are unclear. Use at your won risk.
