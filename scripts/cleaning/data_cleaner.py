# scripts/data_cleaning.py

import pandas as pd
import json
import logging
import psycopg2
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_raw_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def clean_data(raw_data):
    df = pd.DataFrame(raw_data)
    
    # Remove duplicates
    df.drop_duplicates(subset='id', inplace=True)
    
    # Handle missing values
    df.fillna('', inplace=True)
    
    # Standardizing formats (e.g., dates)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    return df

def save_cleaned_data(df):
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(
            dbname='Ethiopian_Medical_Data',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        # Insert cleaned data into the database
        for index, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO suppliers (name, contact_info, created_at)
                VALUES (%s, %s, %s)
                """,
                (row['name'], row['contact_info'], row['date'])
            )

        conn.commit()
        cur.close()
        logging.info("Cleaned data saved to the database successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error while saving cleaned data: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    # Specify the raw data path
    raw_data_path = r'C:\Users\hayyu.ragea\AppData\Local\Programs\Python\Python312\Ethiopian_Medical_Data\data\raw\telegram_data\raw_data.json'
    raw_data = load_raw_data(raw_data_path)
    cleaned_data = clean_data(raw_data)
    save_cleaned_data(cleaned_data)
    logging.info("Data cleaning complete. Cleaned data saved.")
