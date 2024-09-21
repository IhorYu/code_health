import sqlite3

def get_user_data(user_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"  # Potential SQL Injection
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
