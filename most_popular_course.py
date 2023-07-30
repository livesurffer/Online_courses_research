#!/usr/bin/python
import csv
import psycopg2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


db_params={"host":"127.0.0.1","database":"postgres","user":"barmin","password":"barmin"}

conn=psycopg2.connect(**db_params)
cur=conn.cursor()

table_name='online_courses_research'
query = f"select online_courses, count(*) as count from {table_name} group by online_courses order by count desc;"
cur.execute(query)
column_names = cur.fetchall()
x,y=zip(*column_names)
course_dict={}
for i in range(len(x)):
	if ';' in x[i]:
		sep_names=x[i].split(sep=';')
		for course_name in sep_names:
			if course_name in course_dict:
				exist_value=course_dict[course_name]
				course_dict[course_name]=exist_value+y[i]
			else:
				course_dict[course_name]=y[i]		
	else:
		if x[i] in course_dict:
			amount_of_course=course_dict[x[i]]
			course_dict[x[i]]=amount_of_course + y[i]
		else:
			course_dict[x[i]]=y[i]

total_sum = sum(course_dict.values())
#print(total_sum)
percentage={x:round(((y/total_sum)*100),1) for x,y in course_dict.items()}
#print(percentage)
#print(course_dict)

cur.close()
conn.close()
		

plt.figure(figsize=(10, 11))  
plt.pie(percentage.values(), labels=percentage.keys(), autopct='%1.2f%%', startangle=140)

plt.title('Most popular online courses based StackOverFlow survey 2023')
plt.axis('equal')  

plt.savefig('/home/acronym/data_analysis/online_courses_research/course_pie.png')

