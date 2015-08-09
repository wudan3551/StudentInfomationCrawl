##简介
一个简单的网页数据抓取程序，实现了抓取东大研究生学生信息网的学生数据，包括学生姓名、性别、籍贯、本科学校、学院、专业、导师等等信息，将抓取到的网页利用 **python** 做分析，提取出数据并存储到 **MySQL** 数据库中


##系统配置
  **Debian 7.8** , **32-bits Machine**

##前期准备
1. install **python** and **MySQL** in your system
  - **sudo apt-get install python**
  - **sudo apt-get install mysql-client mysql-server** # not very sure about this , if failed , you might need to google it
2. install python libs , you may following the **Installation Guide** part of this - **[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)** , or tack my solution:
  - get a python script called **get-pip.py**
  - run it as root then you finished install **pip**
  - **pip install beautifulsoup4**

##程序实现
[my program](./getStudentInfo.py) mainly consist of 3 part : **web page crawl** , **student information parsing** , **store information into MySQL**

####pre-works
> import urllib # for crawl the web page 
> from bs4 import BeautifulSoup # for parsing student information 
> import MySQLdb # for connect MySQL database 
> import time #for delay 

####web page crawl
```python
theURL = "the url that can fetch student infomation"
f = urllib.urlopen(theURL) # "open" the url
htmlContent = f.read() # get .html from the url
f.close() # "close" the url
```
####student information parsing
```python
soup = BeautifulSoup(htmlContent,'html.parser');
```

