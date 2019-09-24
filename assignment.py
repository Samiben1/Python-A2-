import openpyxl
import sqlite3

wb1 = openpyxl.load_workbook("inspections.xlsx")
wb2 = openpyxl.load_workbook("violations.xlsx")

sheet1 = wb.active
sheet2 = wb.active

print(sheet1)