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

##����ʵ��
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

