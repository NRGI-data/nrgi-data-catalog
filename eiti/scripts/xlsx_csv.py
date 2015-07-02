#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script to convert EITI dataset from XLSX to CSV

import xlrd
import unicodecsv

INFILE = "Copy of EITI Dataset_12Mar2015_dmi_gc_notypos2_IMF.xlsx"
 
def convert_sheet(wb, sheet_name):
    sh = wb.sheet_by_name(sheet_name)
    with open("output/%s.csv" % sheet_name, 'wb') as f:
        c = unicodecsv.writer(f)
        for r in range(sh.nrows):
            c.writerow(sh.row_values(r))

def convert_workbook(filename):
    with xlrd.open_workbook(filename) as wb:
        sheet_names = wb.sheet_names()
        for sheet_name in sheet_names:
            convert_sheet(wb, sheet_name)

if __name__ == '__main__':
    convert_workbook(INFILE)