#!/usr/bin/env python
# -*- coding: gb2312 -*-  # key point 1(add this line in every python script)

import MySQLdb

db = MySQLdb.connect(host='localhost',
		     user='root',
		     passwd='382395',
		     db='StudentInfo',
		     charset='utf8') #thus , we can read utf8 string "from" database

cursor = db.cursor()

name = u"觉得撒" # key point 2(a 'u' befrore chinese character)
print name
#field = name.encode('utf8')
queryStatement = "insert into StudyInfo values(1312," + '"' + name + '"' + ");"
print queryStatement
cursor.execute(queryStatement)
db.commit()

cursor.close()
db.close()
