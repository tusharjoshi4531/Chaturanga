import mysql
from mysql import connector as mc

import pickle

import os


def open_database(Passwd):
    try:
        global connection
        connection = mc.connect(host="localhost", user="root", passwd=Passwd)
    except:
        return False

    global curs
    curs = connection.cursor()

    try:
        curs.execute("CREATE DATABASE chaturanga")
    except:
        pass

    curs.execute("USE chaturanga")
    return True


def create_table(table_name):

    curs.execute(
        "CREATE TABLE %s(Name varchar(255) UNIQUE,  Gdate date, Result varchar(10)) " % (table_name,))


def get_tables():
    curs.execute('SHOW TABLES')

    t = curs.fetchall()
    tables = []

    for i in t:
        tables.append(i[0])

    return tables


def get_games(table_name):
    curs.execute('SELECT name from %s' % (table_name,))

    t = curs.fetchall()
    games = []

    for i in t:
        games.append(i[0])

    return games


def save(name, date, result, game, table_name):

    curs.execute("INSERT INTO %s VALUES('%s','%s','%s') " %
                 (table_name, name, date, result))
    connection.commit()

    try:
        os.mkdir('./data/%s' % (table_name,))
    except:
        pass

    with open('./data/%s/%s.bin' % (table_name, name), "wb") as f:
        pickle.dump(game, f)

def delete_game(name, table_name):

    curs.execute("DELETE FROM %s WHERE NAME = '%s'" % (table_name, name))
    connection.commit()

    os.remove('./data/%s/%s.bin' % (table_name, name))

def delete_table(table_name):

    curs.execute("SELECT NAME FROM %s" % (table_name,))

    games = curs.fetchall()

    for i in games:
        delete_game(i[0], table_name)

    try:
        os.rmdir('./data/%s' % (table_name,))
    except:
        pass

    curs.execute("DROP TABLE %s" % (table_name,))


def load(name, table_name):
    try:
        curs.execute(
            "SELECT Name, GDate, Result FROM %s WHERE name = '%s'" % (table_name, name))
        name, date, result = curs.fetchall()[0]
    except:
        return '', '', '', [{}]

    with open("./data/%s/%s.bin" % (table_name, name), "rb") as f:
        game = pickle.load(f)

    return name, date, result, game
