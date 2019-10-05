# Note: To run the file use conda or install pip module

import sqlite3
import pandas as p

# Variables with database name and spreadsheet file name
database = 'database.db'
excel1 = 'inspections.xlsx'
excel2 = 'violations.xlsx'

# Making connection to a new database
c = sqlite3.connect(database)

print('loading ...')

# Reading the file 1 and adding it corresponding to the database
w1 = p.read_excel(excel1)
w1.to_sql('inspections', c, if_exists='replace', index=False)

print('reading second file...')

# Reading file 2 and adding it correspondingly to database
w2 = p.read_excel(excel2)
w2.to_sql('violations', c, if_exists='replace', index=False)

# printing the database table structure
print("Table structure for the added files in the database")
print("Inspections Table")
print(p.read_sql('PRAGMA table_info(inspections);', c))
print("Violations Table")
print(p.read_sql('PRAGMA table_info(violations);', c))

# database connection cloes
c.close()