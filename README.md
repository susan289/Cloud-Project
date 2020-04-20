
**Version 1.0**


## Project Name

Development of Weather API Using Python

## How to use


1. Install Python and Flask
	python --version
	pip --version
	pip install flask
	
2. Unzip the source code and put it in any folder.
3. Open the terminal or console and then type python rest-server.api

	The app should be up and running

	Access the API with http://localhost:5000/weather/api/v1.0

4. You can find the complete specification of the API at the WSpecification.html file

5. Added a service to add new user with hash MD5 enabled password.Default password is same as username

## License
Susan Yousefi, QMUL






## DB Schema:

mysql> use mydb;
Database changed
mysql> show tables;
+----------------+
| Tables_in_mydb |
+----------------+
| app_users      |
+----------------+
1 row in set (0.00 sec)

mysql> desc app_users;
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| user_id  | int          | NO   | PRI | NULL    | auto_increment |
| username | varchar(255) | NO   |     | NULL    |                |
| password | varchar(255) | NO   |     | NULL    |                |
| Email    | varchar(255) | YES  |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
4 rows in set (0.00 sec) 
