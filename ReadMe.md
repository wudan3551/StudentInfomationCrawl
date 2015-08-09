##简介
一个简单的网页数据抓取程序，实现了抓取东大研究生学生信息网的学生数据，包括学生姓名、性别、籍贯、本科学校、学院、专业、导师等等信息，将抓取到的网页利用 **python** 做分析，提取出数据并存储到 **MySQL** 数据库中


##系统配置
  **Debian 7.8** , **32-bits Machine**

##前期准备
1. install **python** and **MySQL** in your system
  - **sudo apt-get install python**
  - **sudo apt-get install mysql-client mysql-server** # not very sure about this , if failed , you might need to google it
2. install python libs , you may following the **Installation Guide** part of this - **[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)** , or tack my solution:
  - get a python script called [get-pip.py](./get-pip.py)
  - run it as root then you finished install **pip**
  - **pip install beautifulsoup4**
3. install python mysql driver
  - **sudo apt-get install python-mysqldb**

##程序原理
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

##后记
1. 非东大人员IP不是内网IP，不能访问学生信息网站。
2. 由于网页中很多信息是中文的，需要在**python**和**MySQL**中设置编码格式，在我的文件中的第二行设置了`# -*- coding: gb2312 -*-`，
这样python脚本就能将中文数据写入到MySQL中了，而在MySQL中需要在建立数据库是在后面加上`charcter set utf8`，[这里](./createStudyInfoTable.sql)还有[这里](./createPersonalInfoTable.sql)有我的建立数据库中table的格式.
3. 目前程序还有一些**bug**，例如抓取一定数量(30个)的学生数据后就停止了，不知道是内存不足了还是程序其他地方出错造成的.
4. 目前程序中使用的是python自带的parser，还有另一个第三方的parser据说很好用，叫做**lxml**，以后有时间可以看看.
5. 拿到一定量数目的数据后，我们可以对数据做简单分析，例如查看学生籍贯的分布情况，查看学生男女比例，查看学生年龄分布等等，目前暂时想到用类似这样的语句来获取分析结果,获取湖南省学生信息：`select * from personalInfo where HomeTown like "%湖南%";` 
