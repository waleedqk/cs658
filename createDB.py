#!/usr/bin/python3

import sqlite3


conn = sqlite3.connect('macatch.db')
c = conn.cursor()

c.executescript('''
DROP TABLE IF EXISTS cellPhone;
DROP TABLE IF EXISTS cellInstance;

CREATE TABLE IF NOT EXISTS cellPhone (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS cellInstance (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	cellPhone_id INTEGER,
	dateTime TEXT
);
''')

def create_cellPhones_table():
	c.execute('DROP TABLE IF EXISTS cellPhone')
	conn.commit()

	c.execute('''CREATE TABLE IF NOT EXISTS cellPhone
		(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		name TEXT UNIQUE)''')
	conn.commit()

def create_instance_table():
	c.execute('DROP TABLE IF EXISTS cellInstance')
	conn.commit()

	c.execute('''CREATE TABLE IF NOT EXISTS cellInstance
		(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		cellPhone_id INTEGER,
		dateTime TEXT)''')
	conn.commit()

#create_cellPhones_table()
#create_instance_table()
c.close()