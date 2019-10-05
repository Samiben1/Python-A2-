import sqlite3
import numpy as np
import pandas as p
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# connecting the database
database = "database.db"
con = sqlite3.connect(database)
c = con.cursor()


# creating dataframe's


# for highest violating postcode facility
dataframe1 = p.read_sql_query(
    """
    select 
        strftime('%m', ins.activity_date) as month, ins.facility_zip as zip, count(*) as count
	from 	
	    inspections as ins
	where 	
	    ins.facility_zip =(
		    select 
		        i.facility_zip as zip
			from 
			    inspections as i
			where 
			    i.serial_number in (
			        select 
			            serial_number 
			        from 
			        violations
			    )
			group by 
			    i.facility_zip
			order by 
			    count(*) desc
			)
	AND
		ins.serial_number in (
		    select 
		        serial_number 
		    from 
		    violations
		)

	group by 
	    month;
    """, con
)


# for lowest violating postcode facility
dataframe2 = p.read_sql_query(
    """
        select 
            strftime('%m', ins.activity_date) as month, ins.facility_zip as zip, count(*) as count
	    from 	
	        inspections as ins
	    where 	
	        ins.facility_zip =(
		        select 
		            i.facility_zip as zip
				from 
				    inspections as i
				where 
				    i.serial_number in (
				        select 
				            serial_number 
				        from 
				            violations
				    )
					group by 
					    i.facility_zip
					order by 
					    count(*)
            )
			and
				ins.serial_number in (
				    select 
				        serial_number 
				    from 
				        violations
				)
            group by 
                month;
			 """, con)


# for all california average
dataframe3 = p.read_sql_query(
    """
		select 
		    t.month as month, avg(t.count) as average
		from (
			select 
			    strftime('%m', i.activity_date) as month, i.facility_zip as zip, count(*) as count
			FROM 
			    inspections i
			where 
			    i.facility_state = 'CA' and i.serial_number in (
			                                                    select 
			                                                        serial_number 
			                                                    from 
			                                                        violations
			                                                    )
			group by 
			    strftime('%m', i.activity_date), i.facility_zip
		) as t
		group by 
		    t.month;
	""", con)


# for McDonalds violations
dataframe4 = p.read_sql_query(
    """
		select 
		    t.month as month, t.name as name, avg(t.count) as average
		from (
			select 
			    strftime('%m', i.activity_date) as month, i.facility_name as name, count(*) as count
			from 
			    inspections i
			where 
			    i.facility_name like '%mcdonalds%' COLLATE NOCASE AND i.serial_number IN (
			                                                                                select 
			                                                                                    serial_number 
			                                                                                from 
			                                                                                    violations
			                                                                                )
			group by 
			    strftime('%m', i.activity_date), i.facility_zip
		) as t
		group by 
		    t.month;
	""", con)


# for Burger Kings violations
dataframe5 = p.read_sql_query(
    """
		select 
		    t.month as month, t.name as name, avg(t.count) as average
		from (
			select 
			    strftime('%m', i.activity_date) as month, i.facility_name as name, count(*) as count
			from 
			    inspections i
			where 
			    i.facility_name like '%burger king%' COLLATE NOCASE AND i.serial_number IN (
			                                                                                select 
			                                                                                    serial_number 
			                                                                                from 
			                                                                                    violations
			                                                                                )
			group by 
			    strftime('%m', i.activity_date), i.facility_zip
		) as t
		group by 
		    t.month;
	""", con)


# creating graph's based on the dataframe thus obtained
graph = plt.figure()

gs = GridSpec(2, 3)

axis1 = graph.add_subplot(gs[0, 0])
axis2 = graph.add_subplot(gs[0, 1])
axis3 = graph.add_subplot(gs[0, 2])
axis4 = graph.add_subplot(gs[1, :])

axis1.title.set_text("Max Violation PostCode")
axis2.title.set_text("Min Violation PostCode")
axis3.title.set_text("All California Average")
axis4.title.set_text("McDonald's vs. Burger King")

dataframe1.plot(ax=axis1, kind="bar", x="month", y="count", label=dataframe1.iloc[0]['zip'])
dataframe2.plot(ax=axis2, kind="bar", x="month", y="count", label=dataframe2.iloc[0]['zip'])
dataframe3.plot(ax=axis3, kind="line", x="month", y="average")
axis3.get_legend().remove()

dataframe4['Key'] = 'trail1'
dataframe5['Key'] = 'trail2'
DF = p.concat([dataframe4, dataframe5], keys=['trail1', 'trail2'])
DFGroup = DF.groupby(['month', 'Key'])
DFGPlot = DFGroup.sum().unstack('Key').plot(ax=axis4, kind='bar')
L = plt.legend()
L.get_texts()[0].set_text("McDonald's")
L.get_texts()[1].set_text("Burger King")

axis1.set_ylabel('violations')
axis2.set_ylabel('violations')
axis3.set_ylabel('avg violations')
axis4.set_ylabel('avg violations')

graph.tight_layout()

plt.show()
con.close()
