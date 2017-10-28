import psycopg2
import config
import pandas as pd
import csv
from itertools import islice

import os

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


cfg = config.read()
host = cfg.get("postgres","host")
database = "news"
user = cfg.get("postgres","user")
password = cfg.get("postgres","password")
table = "gnews_search_results"


def _getpostgres_connection():
    """
    """
    conn_str = "host={} dbname={} user={} password={}".format(host, database, user, password)
    conn = psycopg2.connect(conn_str)
    
    return conn


def postgres_to_dataframe():
    """

    """
    conn = _getpostgres_connection()
    return pd.read_sql('select * from ' + table, con=conn)



# create table in postgres
# 'CREATE TABLE "similarity"(index1 varchar(20) 
#  NOT NULL, index2 varchar(20) NOT NULL, sim varchar(20) NOT NULL)'

def csv_to_postgres(csv_path):
    """
    
    Arguments:
    - `csv_path`:
    """
    conn = _getpostgres_connection()    
    cur = conn.cursor()

    delete = """Drop table if exists similarity"""
    cur.execute(delete)

    cur.execute("Create Table similarity(index1 varchar(20), index2 varchar(20), similarity varchar(20));")
    conn.commit()

    csv_path = os.path.abspath(csv_path)
    cur.execute("COPY similarity FROM '"+ csv_path + "' DELIMITERS ',';")
    conn.commit()
    
    cur.close()
    conn.close()
