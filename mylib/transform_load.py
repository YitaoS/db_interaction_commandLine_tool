import csv
import os
from dotenv import load_dotenv
from databricks import sql

def load(customers_dataset="Data/customers.csv", orders_dataset="Data/orders.csv"):
    """Transforms and Loads data into the local databricks database"""
    
    # Load customers data
    customers_payload = csv.reader(open(customers_dataset, newline=""), delimiter=",")
    next(customers_payload)  # Skip header

    # Load orders data
    orders_payload = csv.reader(open(orders_dataset, newline=""), delimiter=",")
    next(orders_payload)  # Skip header

    load_dotenv()
    with sql.connect(
        server_hostname=os.getenv("SERVER_HOSTNAME"),
        http_path=os.getenv("HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_KEY"),
    ) as connection:
        with connection.cursor() as cursor:
            # Create the customers table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT,
                customer_name STRING,
                city STRING
            );
            """)
            # Insert data into customers table
            customers_sql = "INSERT INTO customers VALUES"
            for i in customers_payload:
                customers_sql += "\n" + str(tuple(i)) + ","
            customers_sql = customers_sql[:-1] + ";"
            cursor.execute(customers_sql)

            # Create the orders table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT,
                customer_id INT,
                product STRING,
                amount FLOAT,
                order_date STRING
            );
            """)
            # Insert data into orders table
            orders_sql = "INSERT INTO orders VALUES"
            for i in orders_payload:
                orders_sql += "\n" + str(tuple(i)) + ","
            orders_sql = orders_sql[:-1] + ";"
            cursor.execute(orders_sql)

            cursor.close()
        connection.close()

if __name__=="__main__":
    load()