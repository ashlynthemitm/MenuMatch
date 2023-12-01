from dotenv import load_dotenv
import mysql.connector
import os 
import re

class DatabaseConnectionClass():
    def __enter__(self):
        try:
            load_dotenv()
            host_db = os.getenv('DB_HOST')
            username_db = os.getenv('DB_USERNAME')
            password_db = os.getenv('DB_PASSWORD')
            self.db = mysql.connector.connect(
                host=host_db,
                user=username_db,
                password=password_db,
                database='menumatchdb'
            )
            self.cursor = self.db.cursor()
            return self
        except mysql.connector.Error as error:
            print(f'Error: {error}')
        finally:
            self.db.commit()
            print('Saved')
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f'Exception Type: {exc_type}')
            print(f'Exception Value: {exc_value}')
        self.cursor.close()
        self.db.close()
        
    def checkUserId(self, user_id):
        check_id_query = f"""SELECT COUNT(*)
        FROM User
        WHERE user_id = {user_id};"""
        self.cursor.execute(check_id_query)
        results = self.cursor.fetchall()
        ans = results[0][0]
        print(results)
        if ans:
            return True # user_id is in the table
        else:
            return False # user_id is not in the table
        