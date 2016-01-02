#!/usr/bin/env python
# -*- coding: gb2312 -*-  #here change encode to gb2312

import urllib
from bs4 import BeautifulSoup
import MySQLdb
import time
from datetime import datetime # for get current year and month

# define a function to get infromation from soup by id of html
def getContentByID(soup,ID):
    temp = soup.find("span",id=ID)
    return temp.string

# Main Start Here

# Get a Database Connection
db = MySQLdb.connect(host='localhost',
             user='root',
             passwd='382395',
             db='StudentInfo',
             charset='utf8')
cursor = db.cursor()

# Get Current Max Student Id in Two Table of Database
cursor.execute("SELECT MAX(id) FROM StudyInfo")
max_id1 = (cursor.fetchone())[0] # fetch one row(only one row) from result
db.commit()

cursor.execute("SELECT MAX(id) FROM personalInfo")
max_id2 = (cursor.fetchone())[0] #
db.commit()

# make max_id1 equals max_id2
if max_id1 != max_id2:
    if max_id1 == max_id2 - 1:
        cursor.execute("DELETE FROM personalInfo WHERE id = " + str(max_id2))
        db.commit()
    elif max_id1 - 1 == max_id2:
        cursor.execute("DELETE FROM StudyInfo WHERE id = " + str(max_id1))
        db.commit()
    else:
        db.close()
        print "id in two table not match!"
        quit()

# Get The Largest Year , The Year Freshest Students Enrolls
thisYear = datetime.now().year
if(datetime.now().month < 9):
    thisYear = thisYear - 1 # Fresh men have't enroll

# Calculate start_sn and end_sn(Student Number Range)
TotalStudent = 4000
if not max_id1 and not max_id2:
    grade = eval(raw_input("Tell me student of witch year you want to know(a number like 13 - year 2013)"))
    while grade > thisYear and grade <= 0:
        grade = eval(raw_input("Please give a valid number !"))
        
    start_sn = grade * 1000 + 1
    end_sn = start_sn + TotalStudent
else:
    start_sn = max_id1 + 1
    end_sn = (start_sn / 1000) * 1000 + TotalStudent

# Finally , we got what we want - start_sn and end_sn
print "start_sn is " , start_sn
print "end_sn is " , end_sn


print "Start Crawl Data"

try:
    # main loop
    for inputId in range(start_sn,end_sn):
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

            #print Nation;
            #print RollDate;
            #print Source;
            if not ResearchDirection:
                ResearchDirection = u"δ֪"
            if not HomeTown:
                HomeTown = u"δ֪"

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

            if not Source:
                Source = u"δ֪"

            tempstr = "insert into personalInfo values(" + StudentID + ',"' + StudentName + '","' + Sex + '","' + HomeTown + '","' + BirthYear + '","' + Nation + '","' + RollDate + '","' + Source + '")'
            # print tempstr

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

        else :
            print "Invalid Student ID",inputId
        # time.sleep(0.02) # slow down the crawl speed , maybe this can make our crawling like normal website visit
except Exception as excp:
    print "Exception Happened! "
    print type(excp)
    print excp.args
    print excp
finally:
    cursor.close()
    db.close()  # we need to close mysql connect finally
    print "Finish Crawing!"
