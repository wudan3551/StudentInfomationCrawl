#!/usr/bin/env python
# -*- coding: gb2312 -*-  #here change encode to gb2312

import urllib
from bs4 import BeautifulSoup
import MySQLdb
import time

# define a function to get infromation from soup by id of html
def getContentByID(soup,ID):
    temp = soup.find("span",id=ID)
    return temp.string

# main loop
for inputId in range(130031,132032):
	# step 1 : get student information from seu student web page
	#inputId = input('Please Enter a Student ID: ')
	theURL = "http://202.119.4.150/nstudent/ggxx/xsggxxinfo.aspx?xh=" + str(inputId)

	f = urllib.urlopen(theURL)
	htmlContent = f.read()
	f.close()
	soup = BeautifulSoup(htmlContent,'html.parser');

	# step 2 : parsing student information by beautiful soup
	#print "-- Personal Information --"
	StudentID = getContentByID(soup,"lblxh")
	#print "StudentID: ",StudentID

	StudentName = getContentByID(soup,"lblxm")
	#print "StudentName: ",StudentName

	Sex = getContentByID(soup,"lblxb")
	#print "Sex: ",Sex

	HomeTown = getContentByID(soup,"lbljg")
	#print "Home Town: ",HomeTown

	BirthYear = getContentByID(soup,"lblcsrq")
	#print "BirthYear: ",BirthYear

	Nation = getContentByID(soup,"lblmz")
	#print "Nation: ",Nation

	Marriage = getContentByID(soup,"lblhyzk")
	#print "Marriage: ",Marriage

	PoliticalFace = getContentByID(soup,"lblzzmm")
	#print "PoliticalFace: ",PoliticalFace

	RollDate = getContentByID(soup,"lblrxny")
	#print "RollDate: ",RollDate

	Source = getContentByID(soup,"lblksly")
	#print "Source: ",Source

	#temp = soup.find("span",id="lbljtdqm")
	MailPost = getContentByID(soup,"lbljtdqm")
	#print "MailPost: ",MailPost

	#temp = soup.find("span",id="lblrxfs")
	EntryManer = getContentByID(soup,"lblrxfs")
	#print "EntryManer: ",EntryManer

	Education = getContentByID(soup,"lblxl")
	#print "Education: ",Education

	#temp = soup.find("span",id="lblbyyx")
	LastSchool = getContentByID(soup,"lblbyyx")
	#print "LastSchool: ",LastSchool

	#temp = soup.find("span",id="lblybyrq")
	GraduateDate = getContentByID(soup,"lblybyrq")
	#print "GraduateDate: ",GraduateDate

	#temp = soup.find("span",id="lblsflx")
	isStudyAboard = getContentByID(soup,"lblsflx")
	#print "isStudyAboard: ",isStudyAboard

	#temp = soup.find("span",id="lblzymc")
	Major = getContentByID(soup,"lblzymc")
	#Major = temp.string
	#print "Major: ",Major

	#temp = soup.find("span",id="lbldsxm")
	Tutor = getContentByID(soup,"lbldsxm")
	#Tutor = temp.string
	#print "Tutor: ",Tutor

	#temp = soup.find("span",id="lblxwlx")
	academicDegree = getContentByID(soup,"lblxwlx")
	#academicDegree = temp.string
	#print "academicDegree: ",academicDegree

	#temp = soup.find("span",id="lblyjfx")
	#ResearchDirection = temp.string
	ResearchDirection = getContentByID(soup,"lblyjfx")
	#print "ResearchDirection: ",ResearchDirection

	#temp = soup.find("span",id="lblyx")
	#School = temp.string
	School = getContentByID(soup,"lblyx")
	#print "School: ",School

	# if StudentName not empty store data
	if StudentName:
		#step 3: store data into mysql database
		db = MySQLdb.connect(host='localhost',
				     user='root',
				     passwd='382395',
				     db='StudentInfo',
				     charset='utf8')

		cursor = db.cursor()

		cursor.execute("insert into StudyInfo values(" + StudentID + ","
				+ '"' + StudentName + '"' + ","
				+ '"' + Sex + '"' + ","
				+ '"' + LastSchool + '"' + ","
				+ '"' + School + '"' + ","
				+ '"' + Major + '"' + ","
				+ '"' + Tutor + '"' + ","
				+ '"' + ResearchDirection + '"'
				+ ")")
		db.commit()

		cursor.execute("insert into personalInfo values(" + StudentID + ","
				+ '"' + StudentName + '"' + ","
				+ '"' + Sex + '"' + ","
				+ '"' + HomeTown + '"' + ","
				+ '"' + BirthYear + '"' + ","
				+ '"' + Nation + '"' + ","
				+ '"' + RollDate + '"' + ","
				+ '"' + Source + '"'
				+ ")")
		db.commit()

		cursor.close()
		db.close()
	else :
		print "Invalid Student ID",inputId
	time.sleep(1) # slow down the crawl speed , maybe this can make our crawling like normal website visit
