#!/usr/bin/python
import psycopg2
from pandas import DataFrame

# pass in the connection string
class pgconnect():
	@staticmethod
	def connect(str):
		global cursor
		conn_string = str
		# print the connection string we will use to connect
		# print( "Connecting to database\n	->%s" % (conn_string))
		# get a connection, if a connect cannot be made an exception will be raised here
		conn = psycopg2.connect(conn_string)
		# conn.cursor will return a cursor object, you can use this cursor to perform queries
		cursor = conn.cursor()
		return cursor
	# query the tables using query string 
	@staticmethod
	def query(q_str):
		# define query
		query_string = q_str
		# execute our Query
		cursor.execute(query_string)
		# retrieve the records from the database
		df = DataFrame(cursor.fetchall())
		colnames = [desc[0] for desc in cursor.description]
		df.columns = colnames
		return df