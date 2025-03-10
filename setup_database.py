import os
import pyodbc
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Database connection parameters
server = os.getenv('DB_SERVER', 'localhost')
database = os.getenv('DB_NAME', 'jpbank086')
trusted_connection = os.getenv('DB_TRUSTED_CONNECTION', 'yes')
driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')

# Create connection string
conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}'

def execute_sql_file(filename):
    # Read SQL file
    with open(filename, 'r') as file:
        sql_script = file.read()
    
    # Split into individual statements
    statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
    
    # Connect and execute
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Drop existing tables if they exist
        tables = [
            'tbl_transactions_086',
            'tbl_kyc_086',
            'tbl_account_details_086',
            'tbl_users_086',
            'tbl_employees_086',
            'tbl_user_roles_086',
            'tbl_customers_086'
        ]
        
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                conn.commit()
            except Exception as e:
                print(f"Error dropping table {table}: {e}")
        
        # Create tables
        for statement in statements:
            try:
                cursor.execute(statement)
                conn.commit()
            except Exception as e:
                print(f"Error executing statement: {e}")
                print("Statement:", statement)
                continue
        
        print("Database setup completed successfully!")
        
    except Exception as e:
        print(f"Database connection error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    execute_sql_file('create_tables.sql')
