import MySQLdb
import sys

connection = MySQLdb.connect(host = "localhost" , user = "root", passwd = "enixta@123", db = "production")
cursor = connection.cursor()

cursor.execute("show tables")
table = cursor.fetchall()
for x in table:
	query = "SELECT count(*) from {}".format(x[0])
	cursor.execute(query)
	print x[0], cursor.fetchall()[0][0]
