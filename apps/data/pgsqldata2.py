import os
import pandas as pd
import psycopg2 as pg

def readfile(pathfile):
    with open(pathfile, 'r', encoding = "ISO-8859-1") as fd:
        sqlFile = fd.read()
        fd.close()
    return sqlFile

def pgsql_to_df(sqltext):
    with pg.connect("dbname='sar' user='viewer' host='91.197.58.58' port='5432' password='123reader456'") as conn:
        cur = conn.cursor()
        print(cur.connection.status)
        cur.execute(sqltext)
        colnames = [desc[0] for desc in cur.description]
        df = pd.DataFrame(cur.fetchall(), columns=colnames)
    return df


if __name__ == '__main__':

    files = [f for f in os.listdir('./qry') if f.endswith('.sql')]
    print(files)
    for fl in files:
        txt = readfile(f"./qry/{fl}")
        res = pgsql_to_df(txt)
        res.to_csv(f"./{fl.replace('.sql', '.csv')}", index=False, header=True)
        print(f'Done extract data from qry: {fl}')
    print('End extract')
