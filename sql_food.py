import sqlite3

# database connection
database = 'database.db'
con = sqlite3.connect(database)
c = con.cursor()

# sql statements to be executed
c.execute("drop table if exists 'Previous Violations';")
c.execute(
    """
    create table if not exists 'Previous Violations'(
        name    string,
        address string,
        zip     string,
        city    string
    );
    """
)

c.execute(
    """
    select 
        i.facility_name, i.facility_address, i.facility_zip, i.facility_city
    from
        inspections as i, violations as v
    where
        v.serial_number = i.serial_number;
    """
)

c.executemany(
    """
    insert into 'Previous Violations' 
        (name, address, zip, city) 
    values 
        (?,?,?,?);
    """, c.fetchall()
)

c.execute("SELECT * FROM 'Previous Violations';")
total = len(c.fetchall())

# Print total businesses in the list
print(total)

c.execute(
    """
        select 
            i.facility_name, i.facility_address, i.facility_zip, i.facility_city, count(*)
        from
            inspections as i , violations as v
        where
            v.serial_number = i.serial_number
        group by
            i.facility_name, i.facility_address, i.facility_zip, i.facility_city
        order by
            count(*);
    """
)

violation_list = c.fetchall()

# Print the list of businesses sorted based on violations
for i in violation_list:
    print(i)

c.close()

