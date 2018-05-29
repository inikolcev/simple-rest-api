# Simple test rest api in python

yum install epel-release
yum install python34-devel.x86_64 python34-pip mariadb mariadb-server mariadb-devel
yum groupinstall -y 'development tools'  
pip install -r requirements.txt  

set env variable SQLALCHEMY_DATABASE_URI to the database connection string  
Get sample database [here](https://github.com/datacharmer/test_db)
