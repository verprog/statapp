## connect to database
import sqlite3
import pandas as pd
import os


# Укажите путь к вашему CSV-файлу
csv_file_path =(os.getcwd()+r'\data\base_result.csv')
# Прочитайте CSV-файл и создайте DataFrame
dfu = pd.read_csv(csv_file_path)

conn = sqlite3.connect("pythonsqlite.sqlite")

##push the dataframe to sql
# dfu.to_sql("my_data", conn, if_exists="replace")
#
# ##create the table
# conn.execute(
#     """
#     create table base_result as
#     select * from my_data
#     """)
cur = conn.cursor()
cur.execute('''
          SELECT *
          FROM my_data
          ''')

df = pd.DataFrame(cur.fetchall()) #, columns=['product_name','price']
print(df)
