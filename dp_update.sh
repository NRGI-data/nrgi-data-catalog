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

# May way to destroy
# # # # cpi
# # # pip install -r ./cpi/scripts/requirements.txt
# # # python ./cpi/scripts/process.py -o ./cpi/data

# # cofog
# pip install -r ./cofog/scripts/requirements.txt
# python ./cofog/scripts/process.py retrieve
# python ./cofog/scripts/process.py export_to_csv
# python ./cofog/scripts/process.py export_to_rdf
# rm -r ./cache

# # corruption perceptions index
# R < ./corruption-perceptions-index/scripts/process.R --no-save

# # finance-vix
# cd finance-vix && bash ./scripts/process.sh

# # Gold prices
# python ./gold-prices/scripts/process.py -o ./gold-prices

# # IMF weo
# pip install -r ./imf-weo/scripts/requirements.txt
# python ./imf-weo/scripts/process.py -o ./imf-weo

# # ICTD
# pip install -r ./ictd/scripts/requirements.txt
# python ./ictd/scripts/process.py -o ./ictd

# # country-codes
# pip install -r ./country-codes/scripts/requirements.txt
# python ./country-codes/scripts/process.py -o ./country-codes

# # language-codes
# pip install -r ./language-codes/scripts/requirements.txt
# python ./language-codes/scripts/process.py -o ./language-codes

rm -r ./tmp
