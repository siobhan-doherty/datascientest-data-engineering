from datetime import date
from dotenv import load_dotenv
import psycopg2
import os


# load secrets from .env file
load_dotenv()
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

# validate
if not (SQL_USERNAME and SQL_PASSWORD):
    raise RuntimeError("Ensure SQL_USERNAME and SQL_PASSWORD are set in .env")

conn = psycopg2.connect(
    database="kennel_v4",
    host="localhost",
    user=SQL_USERNAME,
    password=SQL_PASSWORD,
    port="5432"
)

try:
    cur = conn.cursor()
    cur.execute("SELECT * FROM Dogs LIMIT 10;")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.execute("SELECT * FROM Dogs WHERE DogName = 'Guinness';")
    guinness = cur.fetchall()
    if guinness:
        print("\nGuinness exists \n", guinness)
    else:
        cur.execute("""
            INSERT INTO Dogs (
                DogName, BreedId, DogGender, DogTattooNumber, DogBirthDate,
                DogCoatColor, ClientId, SalePrice, SaleDate
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            'Guinness', 1, True, '12345', date(2000, 1, 1),
            'Black', 1, 750, date(2005, 1, 1)
        ))
        conn.commit()
        print("\nGuinness is in the Dogs table now")
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")
finally:
    cur.close()
    conn.close()
