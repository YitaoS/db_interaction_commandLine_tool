import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import re
from mylib.transform_load import load
from mylib.query import query


class TestQueryFunction(unittest.TestCase):
    @patch("databricks.sql.connect")  # Mock the sql.connect call
    @patch("dotenv.load_dotenv")
    @patch.dict(
        os.environ,
        {
            "SERVER_HOSTNAME": "mock_hostname",
            "HTTP_PATH": "mock_http_path",
            "DATABRICKS_KEY": "mock_key",
        },
    )
    def test_query(self, mock_load_dotenv, mock_sql_connect):
        # Define a mock SQL query
        mock_sql_string = "SELECT * FROM mock_table LIMIT 5;"

        # Create a mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_sql_connect.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Mock the result of the SQL execution
        mock_cursor.fetchall.return_value = [
            (1, "Sample Product", 100.0, "2024-10-01"),
            (2, "Another Product", 200.0, "2024-10-02"),
        ]

        # Call the query function with the mock SQL string
        query(sql_string=mock_sql_string)

        # Check if the cursor executed the correct SQL command
        mock_cursor.execute.assert_called_once_with(mock_sql_string)

        # Check if the cursor's fetchall method was called
        mock_cursor.fetchall.assert_called_once()

        # Check if the cursor and connection were closed
        mock_cursor.close.assert_called()
        mock_connection.close.assert_called()


class TestLoadFunction(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="customer_id,customer_name,city\n1,John Doe,New York\n2,Jane Smith,Los Angeles\n",
    )
    @patch("databricks.sql.connect")  # Mock the sql.connect call
    @patch("dotenv.load_dotenv")
    @patch.dict(
        os.environ,
        {
            "SERVER_HOSTNAME": "mock_hostname",
            "HTTP_PATH": "mock_http_path",
            "DATABRICKS_KEY": "mock_key",
        },
    )
    def test_load(self, mock_load_dotenv, mock_sql_connect, mock_open):
        # Create a mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_sql_connect.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Mock the orders CSV file
        mock_open.return_value.read_data = """order_id,customer_id,product,amount,
            order_date\n1,1,Laptop,1200,2024-10-01\n2,2,Tablet,600,2024-10-02\n"""

        # Call the function
        load(customers_dataset="Data/customers.csv", orders_dataset="Data/orders.csv")

        # Capture the actual call arguments for debugging
        actual_calls = [call[0][0] for call in mock_cursor.execute.call_args_list]
        print("\nActual SQL calls:")
        for actual_sql in actual_calls:
            print(actual_sql)

        # Define the expected SQL commands
        expected_customer_table_query = """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT,
            customer_name STRING,
            city STRING
        );
        """
        expected_orders_table_query = """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT,
            customer_id INT,
            product STRING,
            amount FLOAT,
            order_date STRING
        );
        """

        # Normalize the whitespace for comparison
        def normalize_sql(sql):
            return re.sub(r"\s+", " ", sql.strip())

        # Assertions for customers table creation
        self.assertIn(
            normalize_sql(expected_customer_table_query),
            [normalize_sql(sql) for sql in actual_calls],
        )

        # Assertions for orders table creation
        self.assertIn(
            normalize_sql(expected_orders_table_query),
            [normalize_sql(sql) for sql in actual_calls],
        )

        # Check if the cursor and connection were closed
        mock_cursor.close.assert_called()
        mock_connection.close.assert_called()


if __name__ == "__main__":
    unittest.main()
