import logging
import os
import time
import pandas as pd
import mysql.connector
from telethon.sync import TelegramClient

# Step 1: Setup logging
log_dir = '../logs/'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=os.path.join(log_dir, 'scraping.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info('Starting Telegram Scraping...')

# Step 2: Telegram API credentials
API_ID = '22719059'
API_HASH = '2a3f5d1d5e677274fc404071bb6bf1bd'
PHONE_NUMBER = '+251982161842'

# Step 3: Initialize the Telegram client
client = TelegramClient('session_name', API_ID, API_HASH)

try:
    client.start(phone=PHONE_NUMBER)
    logging.info("Client started successfully.")
except Exception as e:
    logging.error(f"Failed to start client: {str(e)}")

# Step 4: Channels to scrape
channels = [
    'yetenaweg',  # Channel username for Yetenaweg Telegram Channel
    'lobelia4cosmetics'  # Channel username for Lobelia Pharmacy and Cosmetics
]

# Step 5: Directory to store raw scraped data
raw_data_dir = os.path.join('C:\\Users\\hayyu.ragea\\AppData\\Local\\Programs\\Python\\Python312\\Ethiopian_Medical_Data\\data\\raw\\telegram_data')
if not os.path.exists(raw_data_dir):
    os.makedirs(raw_data_dir)

# Step 6: Initialize MySQL database connection
db_connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',  # Update this if your MySQL user is different
    password='',  # Your MySQL password
    database='ethiopian_medial_data'
)

db_cursor = db_connection.cursor()

# Step 7: Create a table for storing messages in MySQL
db_cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    message_id INT PRIMARY KEY,
    date DATETIME,
    sender_id INT,
    message TEXT,
    media ENUM('Yes', 'No')
)
''')
db_connection.commit()

# Step 8: Function to scrape messages and media from Telegram channels
def scrape_channel(channel, limit=100):
    try:
        logging.info(f"Scraping channel: {channel}")
        print(f"Scraping channel: {channel}")
        messages = []
        message_count = 0
        media_downloaded_count = 0

        for message in client.iter_messages(channel, limit=limit):
            message_data = {
                'message_id': message.id,
                'date': message.date,
                'sender_id': message.sender_id,
                'message': message.message,
                'media': 'Yes' if message.media else 'No'
            }
            messages.append(message_data)

            # Step 9: Store message in MySQL database
            db_cursor.execute('''
            INSERT IGNORE INTO messages (message_id, date, sender_id, message, media) 
            VALUES (%s, %s, %s, %s, %s)
            ''', (message_data['message_id'], message_data['date'], message_data['sender_id'],
                  message_data['message'], message_data['media']))
            db_connection.commit()
            message_count += 1

            # Step 10: Download media if available
            if message.media:
                media_file_path = os.path.join(raw_data_dir, f"{channel}_{message.id}.jpg")
                if not os.path.exists(media_file_path):
                    client.download_media(message.media, file=media_file_path)
                    media_downloaded_count += 1
                    logging.info(f"Downloaded media for message ID: {message.id}")
                    print(f"Downloaded media for message ID: {message.id}")
                else:
                    logging.warning(f"Media file already exists for message ID: {message.id}, skipping download.")
                    print(f"Media file already exists for message ID: {message.id}, skipping download.")

        logging.info(f"Scraping completed for channel: {channel}. Total messages scraped: {message_count}, Total media downloaded: {media_downloaded_count}.")
        return pd.DataFrame(messages)

    except Exception as e:
        logging.error(f"Error scraping channel {channel}: {str(e)}")
        print(f"Error scraping channel {channel}: {str(e)}")
        return pd.DataFrame()

# Step 11: Scrape all channels and store data
all_data = pd.DataFrame()
for channel in channels:
    if isinstance(channel, str) and channel:
        channel_data = scrape_channel(channel)
        all_data = pd.concat([all_data, channel_data], ignore_index=True)
        print(f"Data from channel '{channel}' added.")
        time.sleep(5)  # Sleep to avoid hitting rate limits
    else:
        logging.error(f"Invalid channel name: {channel}")

# Step 12: Save the scraped data to CSV
if not all_data.empty:
    csv_file_path = os.path.join(raw_data_dir, 'telegram_scraped_data.csv')
    all_data.to_csv(csv_file_path, index=False)
    logging.info("Scraping completed and data saved to CSV.")
    print("Scraping completed and data saved to CSV.")
else:
    logging.warning("No data was scraped.")
    print("No data was scraped.")

# Step 13: Close the MySQL connection
db_cursor.close()
db_connection.close()
