import mysql.connector

# MySQL database configuration
db_config = {
    'user': 'root',
    'password': '![Dedox--3467',
    'host': '127.0.0.1',  # Use the IP of your MySQL container
    'database': 'scrapper',
    'raise_on_warnings': True,
}

def get_mysql_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None