import mysql.connector
from seed import connect_to_prodev

def stream_users():
    connection = connect_to_prodev()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        row = cursor.fetchone()
        while row is not None:
            yield row
            row = cursor.fetchone()
        
        cursor.close()
        connection.close()