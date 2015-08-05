#!/bin/bash
mkdir tmp
# install pip
# install python
# install R
# install wget
# install mdbtools
# wget https://cran.r-project.org/src/contrib/rvest_0.2.0.tar.gz -O ./tmp/rvest_0.2.0.tar.gz
# wget https://cran.r-project.org/src/contrib/xlsx_0.5.7.tar.gz -O ./tmp/xlsx_0.5.7.tar.gz
# wget https://cran.r-project.org/src/contrib/countrycode_0.18.tar.gz ./tmp/countrycode_0.18.tar.gz
# wget https://cran.r-project.org/src/contrib/reshape2_1.4.1.tar.gz ./tmp/reshape2_1.4.1.tar.gz
# R CMD install ./tmp/rvest_0.2.0.tar.gz
# R CMD install ./tmp/xlsx_0.5.7.tar.gz
# R CMD install ./tmp/countrycode_0.18.tar.gz
# R CMD install ./tmp/reshape2_1.4.1.tar.gz

# # cofog
# pip install -r ./cofog/scripts/requirements.txt
# python ./cofog/scripts/process.py retrieve
# python ./cofog/scripts/process.py export_to_csv
# python ./cofog/scripts/process.py export_to_rdf

# # corruption perceptions index
# R < ./corruption-perceptions-index/scripts/script.R --no-save

# May way to destroy
# # # # cpi
# # # pip install -r ./cpi/scripts/requirements.txt
# # # python ./cpi/scripts/cpi2datapackage.py -o ./cpi/data

# # finance-vix
# cd finance-vix && bash ./scripts/process.sh

# # Gold prices
# python ./gold-prices/scripts/process.py -o ./gold-prices

# IMF weo
python ./imf-weo/scripts/process.py -o ./imf-weo


rm -r ./tmp
