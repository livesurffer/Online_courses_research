#!/usr/bin/python
import csv
import psycopg2

db_params={"host":"127.0.0.1","database":"postgres","user":"barmin","password":"barmin"}

conn=psycopg2.connect(**db_params)
cur=conn.cursor()

csv_file='/home/acronym/data_analysis/Global-research_of_changing_work_model/survey_2022_2023/survey_results_public_2023.csv'
table_name='survey_23'
query = f"SELECT column_name FROM information_schema.columns WHERE table_name ='{table_name}'"
cur.execute(query)
column_names = cur.fetchall()
column_names = [column[0] for column in column_names]
column_names_fin=column_names[1:]

columns_for_analisys=[2,3,4,5]
data_for_insert=[]

with open(csv_file,newline='') as csvf:
	thereader=csv.reader(csvf)
	skipheader=next(thereader)
	for row in thereader:
		filter_row = [row[i] for i in range(2,6)]		
		data_for_insert.append(filter_row)
	column_placeholder = ','.join(['%s'] * len(filter_row))

	insert_query = f"INSERT INTO {table_name} ({','.join(column_names_fin)}) VALUES ({column_placeholder})"
	cur.executemany(insert_query, data_for_insert)
	
conn.commit()

cur.close()
conn.close()		
