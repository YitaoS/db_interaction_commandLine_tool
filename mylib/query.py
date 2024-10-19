import os
from dotenv import load_dotenv
from databricks import sql

complex_query="""
    WITH city_totals AS (
        SELECT
            c.city,
            COUNT(o.order_id) AS total_orders,
            SUM(o.amount) AS total_amount_spent,
            AVG(o.amount) AS avg_order_value
        FROM default.customers c
        JOIN default.orders o ON c.customer_id = o.customer_id
        GROUP BY c.city
    )
    SELECT
        c.customer_name,
        c.city,
        ct.total_orders,
        ct.total_amount_spent,
        ct.avg_order_value
    FROM default.customers c
    JOIN city_totals ct ON c.city = ct.city
    ORDER BY ct.total_amount_spent DESC;
"""
def query(sql_string=complex_query):
    """Query the database for the top 5 rows of the GroceryDB table"""
    load_dotenv()
    with sql.connect(
        server_hostname=os.getenv("SERVER_HOSTNAME"),
        http_path=os.getenv("HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_KEY"),
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_string)
            result = cursor.fetchall()
            
            for row in result:
                print(row)
        cursor.close()
    connection.close()


if __name__=="__main__":
    query()