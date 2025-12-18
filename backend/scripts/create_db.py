import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    # Connect to default database
    try:
        # Try connecting to 'postgres'
        conn = psycopg2.connect(
            dbname="postgres",
            user="user",
            password="password",
            host="localhost",
            port="5432"
        )
    except Exception as e:
        print(f"Failed to connect to 'postgres' db: {e}")
        # Try connecting without password or with different user if needed
        # For now, we assume the config in .env matches
        return

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    db_name = "customer_pulse"
    
    # Check if exists
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
    exists = cur.fetchone()
    
    if not exists:
        print(f"Creating database {db_name}...")
        cur.execute(f"CREATE DATABASE {db_name}")
        print("Database created successfully.")
    else:
        print(f"Database {db_name} already exists.")
        
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_database()
