# /usr/bin/python3.4
__author__ = 'Mertcan Gokgoz'

import pymysql
import sys

try:
    # database connection string
    database = pymysql.connect("localhost", "root", "muratcan22", "panoDB")
    # prepare cursor object this metod
    cursor = database.cursor()

    # drop table if it already exist
    cursor.execute("DROP TABLE IF EXISTS TimeTable")

    # SQL Command line
    sql = """CREATE TABLE TimeTable (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            Types VARCHAR(45) NOT NULL COMMENT '',
            LectureTime VARCHAR(45) NOT NULL COMMENT '',
            LectureTeacher VARCHAR(45) NOT NULL COMMENT '',
            Lesson VARCHAR(45) NOT NULL COMMENT '',
            Place VARCHAR(45) NOT NULL COMMENT '',
            Days VARCHAR(45) NOT NULL COMMENT '')"""

    # execute current sql command from create table
    cursor.execute(sql)
    # disconnect from the server
    database.close()
    print("Database Created")
except Exception as e:
    print("\n[ Error ]\n\t Error Message:\t ", e, "\n")
    sys.exit(1)
