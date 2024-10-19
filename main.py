from mylib.transform_load import load
from mylib.query import query


def main():
    complex_query = """
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
    load()
    query(complex_query)


if __name__ == "__main__":
    main()
