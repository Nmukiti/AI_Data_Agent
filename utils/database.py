import psycopg2


class DatabaseUtil:

    def __init__(self, db_config):
        self.db_config = db_config

        try: 
            self.connection = psycopg2.connect(**db_config) 

        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.connection = None

    def schema_details(self,schema_name):

        schema_info_context = ""
        
        connection = self.connection
        cursor = connection.cursor()

        schema_info_context = f"Database Schema: {schema_name}\n"

        try: 

            cursor.execute("SELECT table_name from information_schema.tables where table_schema = %s;", (schema_name,))
            tables_list = cursor.fetchall()

            for table in tables_list:
                table_name = table[0]
                schema_info_context = f"{schema_info_context}\nTable: {table_name}\n"

                # Adding Columns & Data Types
                cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s;", (table_name,))
                columns_list = cursor.fetchall()

                for column in columns_list:
                    column_name = column[0]
                    data_type = column[1]
                    schema_info_context = f"{schema_info_context}  Column: {column_name}, Data Type: {data_type}\n"

                # Adding Sample Data
                cursor.execute(f"SELECT * FROM {schema_name}.{table_name} LIMIT 5;")
                sample_data = cursor.fetchall()
                schema_info_context = f"{schema_info_context}  Sample Data:\n"
                for row in sample_data:
                    schema_info_context = f"{schema_info_context}    {row}\n"

        except Exception as e:
            print(f"Error fetching schema details: {e}")
            schema_info_context = f"Error fetching schema details: {e}"

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        
        return schema_info_context
    

    def execute_sql(self, query):
        """
        Executes the provided SQL query on the database.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            str: The result of the SQL query execution or an error message if execution fails.
        """
    
        try:
            connection = self.connection
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall() # fetchall() retrieves all rows of a query result, returning them as a list of tuples
            connection.commit() # Commit the transaction to ensure any changes are saved
            return str(result) # convert to string for serialization

        except Exception as e:
            print(f"Error executing SQL query: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()



obj = DatabaseUtil({
    "database": "postgres",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
})

result = obj.schema_details("public")

with open("test_schema_info.txt", "w") as f:
    f.write(result)