import sqlite3
import csv

# connecting the database
database = 'database.db'
con = sqlite3.connect(database)
c = con.cursor()

# new workbook and spreadsheet creation
w = open('ViolationTypes.csv', "w", newline="")
sheet = csv.writer(w)

title = ['Code', 'Description', 'Count']
sheet.writerow(title)
# sql statement executions

c.execute(
    """
        select
            violation_code, violation_description, count(*)
        from
            violations
        group by
            violation_code
        order by
            count(*); 
    """
)
sheet.writerows(c.fetchall())

c.execute("select count(*) from violations;")
sheet.writerow((' ', 'Total Violations', c.fetchone()[0]))

print('Done')
c.close()
