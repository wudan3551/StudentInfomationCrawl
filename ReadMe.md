##���
һ���򵥵���ҳ����ץȡ����ʵ����ץȡ�����о���ѧ����Ϣ����ѧ�����ݣ�����ѧ���������Ա𡢼��ᡢ����ѧУ��ѧԺ��רҵ����ʦ�ȵ���Ϣ����ץȡ������ҳ���� **python** ����������ȡ�����ݲ��洢�� **MySQL** ���ݿ���


##ϵͳ����
  **Debian 7.8** , **32-bits Machine**

##ǰ��׼��
1. install **python** and **MySQL** in your system
  - **sudo apt-get install python**
  - **sudo apt-get install mysql-client mysql-server** # not very sure about this , if failed , you might need to google it
2. install python libs , you may following the **Installation Guide** part of this - **[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)** , or tack my solution:
  - get a python script called **get-pip.py**
  - run it as root then you finished install **pip**
  - **pip install beautifulsoup4**

##����ԭ��
[my program](./getStudentInfo.py) mainly consist of 3 part : **web page crawl** , **student information parsing** , **store information into MySQL**

####pre-imports
```python
import urllib # for crawl the web page 
from bs4 import BeautifulSoup # for parsing student information 
import MySQLdb # for connect MySQL database 
import time #for delay 
```

####web page crawl
```python
theURL = "the url that can fetch student infomation"
f = urllib.urlopen(theURL) # "open" the url
htmlContent = f.read() # get .html file from the url
f.close() # "close" the url
```

####student information parsing

```python
"""define a function to get student info from .html "span" tag"""
def getContentByID(soup,ID):
    temp = soup.find("span",id=ID) #the infomation are inside "span" tag , and their id attribute is differ from each other
    return temp.string

soup = BeautifulSoup(htmlContent,'html.parser');

StudentInfoNumberN = getContentByID(soup,"the id") # then this variable contains strings that you want
```
####store information into database
```python
db = MySQLdb.connect(host='localhost',
		     user='username',
		     passwd='password',
		     db='db name',
		     charset='utf8') #this will set the charset of mysql into utf8 , this is very importent for indicating chinese character

cursor = db.cursor() # i have no idea what this statement means

"""execute a query command in mysql"""
cursor.execute("insert into tablename values(field1_value,field2_value, ... ...)")
cursor.commit()

cursor.close()
db.close()
```
