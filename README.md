# Python-A2-

The file contains four python script files.
1. Createdb_food.py:
	The files creates a new database and creates a dataframe based on the excel files provided to query the data in sql_food.py file.
2. sql_food.py:
	The file queries into inspection and violations table from the two excell files
3. excel_food.py:
	This python script creates a new excel file called "VioltionsTypes" and stores the code, description and violation count along with the total violations.
4. numpy_food.py:
	This file plots the graph based on the data in the database.

Run the scripts

# Note: to run the program in Pycharm, you need to install Pip. It can be done from settings>add module.

It is recomended to use spyder/ conda specially for the running first file (createdb_food.py).

step 1: Run the createdb_food.py: it creates a database and sets tha dataframe for future data's

step 2: Run the sql_food.py: It queries data into the inspection and violation table in the database

step 3:	Run the excel_food.py: It creates a new excel file called "ViolationsTypes" amd stores violations code, description and count.
	 
step 4: Run Numpy_food.py: It generates graphs based on the data provided in the database plotting violations overtime.