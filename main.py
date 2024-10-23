import sys
import argparse
from mylib.transform_load import load
from mylib.query import query


def handle_arguments(args):
    parser = argparse.ArgumentParser(description="ETL and Query CLI Tool")
    parser.add_argument(
        "action",
        choices=["load", "query"],
        help="Specify the action to perform",
    )

    # Temporarily parse known arguments to check the action
    partial_args = parser.parse_args(args[:1])  # Parse only the 'action'

    # Add a query argument if the action is 'query'
    if partial_args.action == "query":
        parser.add_argument(
            "query",
            nargs=argparse.REMAINDER,
            help="SQL query to be executed",
        )

    return parser.parse_args(args)  # Fully parse the arguments


def main():
    args = handle_arguments(sys.argv[1:])

    if args.action == "load":
        print("Loading data...")
        load()
    elif args.action == "query":
        if not args.query:
            print("Error: A query is required for the 'query' action.")
            sys.exit(1)  # Exit the program if no query is provided
        else:
            # Join the SQL query list back into a string
            query_string = " ".join(args.query)
            print(f"Executing query: {query_string}")
            query(query_string)
    else:
        print(f"Unknown action: {args.action}")


if __name__ == "__main__":
    main()
###
# complex_query = """
# WITH city_totals AS (
#     SELECT
#         c.city,
#         COUNT(o.order_id) AS total_orders,
#         SUM(o.amount) AS total_amount_spent,
#         AVG(o.amount) AS avg_order_value
#     FROM default.customers c
#     JOIN default.orders o ON c.customer_id = o.customer_id
#     GROUP BY c.city
# )
# SELECT
#     c.customer_name,
#     c.city,
#     ct.total_orders,
#     ct.total_amount_spent,
#     ct.avg_order_value
# FROM default.customers c
# JOIN city_totals ct ON c.city = ct.city
# ORDER BY ct.total_amount_spent DESC;
# """
###