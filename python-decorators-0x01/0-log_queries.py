import sqlite3
import functools
"from datetime import datetime"

def log_queries(func):
    """Decorator that logs SQL queries before execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", args[0] if args else "")
        print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Test run
users = fetch_all_users(query="SELECT * FROM users")
print(users)
