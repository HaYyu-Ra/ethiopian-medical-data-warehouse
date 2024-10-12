import pandas as pd
from sqlalchemy import create_engine
import logging

# Configure logging
logging.basicConfig(filename='etl_pipeline.log', level=logging.INFO)

def load_data(file_path):
    logging.info('Loading data from CSV file.')
    print("Loading data from CSV file.")
    return pd.read_csv(file_path)

def clean_data(df):
    logging.info('Cleaning data.')
    print("Cleaning data.")
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Handle missing values for numeric columns only
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    
    # Standardize formats (example: convert date columns to datetime)
    if 'date_column' in df.columns:
        df['date_column'] = pd.to_datetime(df['date_column'])
    
    # Data validation (example: check for negative values in a column)
    if 'some_numeric_column' in df.columns:
        assert (df['some_numeric_column'] >= 0).all(), "Negative values found in some_numeric_column"
    
    return df

def save_cleaned_data(df, cleaned_data_path):
    logging.info('Saving cleaned data to CSV file.')
    print("Saving cleaned data to CSV file.")
    df.to_csv(cleaned_data_path, index=False)

def store_data_in_db(df, database_url):
    logging.info('Storing cleaned data in the database.')
    print("Storing cleaned data in the database.")
    engine = create_engine(database_url)
    df.to_sql('cleaned_telegram_data', engine, if_exists='replace', index=False)

def main():
    # File paths
    raw_data_path = r'C:\Users\hayyu.ragea\AppData\Local\Programs\Python\Python312\Ethiopian_Medical_Data\data\raw\telegram_data\telegram_scraped_data.csv'
    cleaned_data_path = r'C:\Users\hayyu.ragea\AppData\Local\Programs\Python\Python312\Ethiopian_Medical_Data\data\cleaned\cleaned_telegram_data.csv'
    
    # Database URL
    database_url = 'postgresql+psycopg2://postgres:admin@localhost:5432/Ethiopian_Medical_Data'
    
    # ETL Process
    logging.info('ETL process started.')
    print("ETL process started.")
    
    # Load data
    df = load_data(raw_data_path)
    
    # Clean data
    df = clean_data(df)
    
    # Save cleaned data
    save_cleaned_data(df, cleaned_data_path)
    
    # Store data in database
    store_data_in_db(df, database_url)
    
    logging.info('ETL process completed.')
    print("ETL process completed.")

if __name__ == "__main__":
    main()
