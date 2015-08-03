#!/bin/bash
mkdir tmp
# install pip
# install python
# install R
# install wget

# install mdbtools
# pip install -r ./cofog/scripts/requirements.txt
# wget https://cran.r-project.org/src/contrib/rvest_0.2.0.tar.gz -O ./tmp/rvest_0.2.0.tar.gz
# R CMD install ./tmp/rvest_0.2.0.tar.gz
# wget https://cran.r-project.org/src/contrib/xlsx_0.5.7.tar.gz -O ./tmp/xlsx_0.5.7.tar.gz
# R CMD install ./tmp/xlsx_0.5.7.tar.gz

# # cofog
# python ./cofog/scripts/process.py retrieve
# python ./cofog/scripts/process.py export_to_csv
# python ./cofog/scripts/process.py export_to_rdf

# corruption
R < ./corruption-perceptions-index/scripts/script.R --no-save
# "./corruption-perceptions-index/scripts/script.sh"

rm -r ./tmp

