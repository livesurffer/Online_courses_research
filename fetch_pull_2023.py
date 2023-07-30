#!/usr/bin/python
import csv
import psycopg2
import time

db_params={"host":"127.0.0.1","database":"postgres","user":"barmin","password":"barmin"}

conn=psycopg2.connect(**db_params)
cur=conn.cursor()

csv_file='/home/acronym/data_analysis/online_courses_research/data_survey_2022_2023/survey_results_public_2023.csv'
table_name='online_courses_research'
query = f"SELECT column_name FROM information_schema.columns WHERE table_name ='{table_name}'"
cur.execute(query)
column_names = cur.fetchall()
column_names = [column[0] for column in column_names]
column_names_fin=column_names[1:]

columns_for_analisys=[3,4,9,10,20,19]
data_for_insert=[]

with open(csv_file,newline='') as csvf:
	thereader=csv.reader(csvf)
	skipheader=next(thereader)
	filtering_row=[]
	for row in thereader:
		filtering_row = [float(int(row[i]),3) if i == 20 and row[i] != 'NA' else None if i == 20 and row[i] == 'NA' else row[i] for i in columns_for_analisys]

		data_for_insert.append(tuple(filtering_row))

column_placeholder = ','.join(['%s'] * len(column_names_fin))
insert_query = f"INSERT INTO {table_name} ({','.join(column_names_fin)}) VALUES ({column_placeholder})"
cur.executemany(insert_query, data_for_insert)
	
conn.commit()

cur.close()
conn.close()		
