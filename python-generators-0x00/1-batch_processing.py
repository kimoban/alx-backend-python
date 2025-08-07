import mysql.connector
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    offset = 0
    connection = connect_to_prodev()
    
    while True:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        batch = cursor.fetchall()
        cursor.close()
        
        if not batch:
            connection.close()
            break
            
        yield batch
        offset += batch_size

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
                ["return"]
