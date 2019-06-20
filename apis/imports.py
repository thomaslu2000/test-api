from flask_restplus import Namespace, Resource, fields
from flask import jsonify, request
import pymysql
from .db_config import db_info
import datetime
import requests
import json


def convert_dates(dic_list):
    """
    takes in a list of dictionaries and turns datetime objects into strings
    we need to do this bc python cant turn datetime objects into json
    """
    if len(dic_list) > 0:
        dates = [k for k, v in dic_list[0].items() if isinstance(v, (datetime.datetime, datetime.date))]
        for date in dates:
            for dic in dic_list:
                dic[date] = str(dic[date])

def make_conn():
    """
    connects to a database
    """
    return pymysql.connect(host=db_info['MYSQL_DATABASE_HOST'],
                             user=db_info['MYSQL_DATABASE_USER'],
                             password=db_info['MYSQL_DATABASE_PASSWORD'],
                             db=db_info['MYSQL_DATABASE_DB'],
                             cursorclass=pymysql.cursors.DictCursor)

def url_exists(path):
    """
    checks if a url exists
    """
    r = requests.head(path)
    return r.status_code == requests.codes.ok

def add_dict_lists(query_response, added_dict_list):
    """
    zips together two lists of dictionaries
    by mutating the first argument
    """
    for i in range(len(query_response)):
        current_dict = query_response[i]
        current_dict_to_add = added_dict_list[i]
        for key, value in current_dict_to_add.items():
            current_dict[key] = value
    
def make_json(list_of_dicts):
    """
    turns a list of dictionaries into a json object with a status code
    """
    resp = jsonify(list_of_dicts)
    resp.status_code = 200
    return resp

def query(query):
    """
    executes an sql query where the 'query' argument is a string
    """
    conn = make_conn()
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        convert_dates(rows)
        conn.commit()
        return rows if rows else cur.lastrowid
    except Exception as e:
        print(e)
        return str(e)
    finally:
        cur.close()
        conn.close()

def make_update_statement(table, val_dict, where_clause):
    """
    this returns a string that forms a generic sql update statement
    where the keys of the provided dictionary are the columns
    and the values are the values
    """
    query = f"UPDATE {table} SET "
    query += ", ".join([f"{key}='{value}'" for key, value in val_dict.items()])
    query += " WHERE " + where_clause
    return query

def make_insert_statement(table, val_dict):
    
    """
    this returns a string that forms a generic sql insert statement
    where the keys of the provided dictionary are the columns
    and the values are the values
    """
    query = f"INSERT INTO {table} ("
    query += ", ".join(val_dict.keys())
    query += ") VALUES ('"
    query += "', '".join(val_dict.values())
    query += "')"
    return query
