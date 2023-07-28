#!/usr/bin/python
import psycopg2
import requests
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Connect to PostgreSQL and retrieve data from table
connection = psycopg2.connect(
    host="127.0.0.1",
    database="postgres",
    user="barmin",
    password="barmin",
    port="5432"
)
cursor = connection.cursor()

query_23 = "select remote, count(*) as count from survey_23 group by remote order by count asc;"
query_22 = "select remote, count(*) as count from survey_22 group by remote order by count asc;"

cursor.execute(query_22)
data_22 = cursor.fetchall()

cursor.execute(query_23)
data_23 = cursor.fetchall()

type_23, number_23 = zip(*data_23)
type_22, number_22 = zip(*data_22)
cursor.close()
connection.close()

data_for_chart_22=[]
for i in number_22:
        if number_22.index(i)==2:
                swap_number=i
        elif number_22.index(i)==3:
                data_for_chart_22.append(i)
                data_for_chart_22.append(swap_number)           
        else:
                data_for_chart_22.append(i)


total_number_22 = sum(number_22)
percentage_22 = [(i/total_number_22)*100 for i in data_for_chart_22]

total_number_23 = sum(number_23)
percentage_23 = [(i/total_number_23)*100 for i in number_23]

name_for_chart = ['Office','No answer','Remote','Hybrid']


# create figure and graph
fig, graph = plt.subplots(figsize=(10,10))

# set width for bars
width = 0.37

x = range(len(name_for_chart))

# graph 2022
bar1 = graph.bar(x, percentage_22, width, label='Data 2022')

# graph 2023
bar2 = graph.bar([i + width for i in x], percentage_23, width, label='Data 2023')

# set labels, title, legend
graph.set_xlabel('Work model')
graph.set_ylabel('Percent of developers')
graph.set_title('Comparison of Data 2022 and 2023')
graph.set_xticks([i + width/2 for i in x])
graph.set_xticklabels(name_for_chart)
graph.legend()

# add % values above each bar
for bar in bar1 + bar2:
    height = bar.get_height()
    graph.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.3f}%', ha='center', va='bottom')

plt.savefig('/home/acronym/data_analysis/Global-research_of_changing_work_model/compare_model_work.png')


