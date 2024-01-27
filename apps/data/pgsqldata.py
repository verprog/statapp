import os
import pandas as pd
import psycopg2 as pg




def readfile(pathfile):
    with open(pathfile, 'r') as fd:
        sqlFile = fd.read()
        fd.close()
    return sqlFile

def pgsql_to_df(sqltext):
    with pg.connect("dbname='sar_16.10' user='postgres' host='127.0.0.1' port='5432' password='dar'") as conn:
        cur = conn.cursor()
        cur.execute(sqltext)
        colnames = [desc[0] for desc in cur.description]
        df = pd.DataFrame(cur.fetchall(), columns=colnames)
    return df


if __name__ == '__main__':

    files = [f for f in os.listdir('./qry') if f.endswith('.sql')]
    for fl in files:
        txt = readfile(f"./qry/{fl}")
        res = pgsql_to_df(txt)
        res.to_csv(f"./qry/{fl.replace('.sql', '.csv')}", index=False, header=True)
        print(f'Done extract data from qry: {fl}')
    print('End extract')
