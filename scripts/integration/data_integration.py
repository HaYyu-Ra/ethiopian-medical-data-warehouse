import pandas as pd
from sqlalchemy import create_engine

# Database connection details
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'Ethiopian_Medical_Data'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'

def fetch_data_from_dbt_models():
    """Fetch data from dbt models and return as DataFrames."""
    try:
        # Create a SQLAlchemy engine
        connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(connection_string)
        print("Database connection successful.")

        # SQL queries to fetch data from dbt models
        query_first_model = "SELECT * FROM analytics.cleaned_data;"  # Change to your actual dbt model name
        query_second_model = "SELECT * FROM analytics.transform_cleaned_data;"  # Change to your actual dbt model name

        # Fetch data from the first model
        df_first_model = pd.read_sql(query_first_model, engine)
        print("Fetched data from cleaned_data:")
        print(df_first_model.head())  # Display the first few rows of the DataFrame

        # Fetch data from the second model
        df_second_model = pd.read_sql(query_second_model, engine)
        print("Fetched data from transform_cleaned_data:")
        print(df_second_model.head())  # Display the first few rows of the DataFrame

        return df_first_model, df_second_model

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    fetch_data_from_dbt_models()
