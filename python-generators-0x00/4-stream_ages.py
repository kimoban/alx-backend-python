import mysql.connector
from seed import connect_to_prodev

def stream_user_ages():
    connection = connect_to_prodev()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        row = cursor.fetchone()
        while row is not None:
            yield row[0]
            row = cursor.fetchone()
        
        cursor.close()
        connection.close()

def calculate_average_age():
    total = 0
    count = 0
    
    for age in stream_user_ages():
        total += age
        count += 1
    
    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found")

if __name__ == "__main__":
    calculate_average_age()