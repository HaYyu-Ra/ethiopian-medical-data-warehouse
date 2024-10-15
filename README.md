# Ethiopian Medical Data Warehouse

## Overview

The Ethiopian Medical Data Warehouse project aims to build a robust and scalable data warehouse that stores data on Ethiopian medical businesses. This data is sourced from various web scraping techniques, primarily through Telegram channels. The project integrates advanced object detection capabilities using YOLO (You Only Look Once) to enhance the data analysis process.

The establishment of this data warehouse significantly improves the data analysis process. Centralizing all data allows the team to conduct comprehensive analyses to uncover valuable insights about Ethiopian medical businesses. This data will help identify trends, patterns, and correlations that are otherwise challenging to detect with fragmented data, leading to better decision-making. A well-structured data warehouse also enhances querying and reporting efficiency, providing actionable intelligence quickly and accurately.

## Business Need

As a data engineer at Kara Solutions, a leading data science company with over 50 data-centric solutions, your task involves several key steps and considerations to ensure the data warehouse is robust, scalable, and capable of addressing the unique challenges associated with scraping and collecting data from Telegram channels.

### Key Components

1. **Data Scraping and Collection Pipeline**: Build a pipeline to scrape data from relevant Telegram channels.
2. **Data Cleaning and Transformation Pipeline**: Develop processes to clean and transform the scraped data for analysis.
3. **Object Detection**: Implement YOLO for analyzing collected images.
4. **Data Warehouse Design and Implementation**: Design and implement a data warehouse to store the processed data.
5. **Data Integration and Enrichment**: Enrich the data for better analysis and insights.

## Project Deliverables

### Task 1 - Data Scraping and Collection Pipeline

- **Telegram Scraping**: Utilize the Telegram API or custom scripts to extract data from public Telegram channels relevant to Ethiopian medical businesses. 
  - Example Channels: 
    - [Yetenaweg](https://t.me/yetenaweg)
  
- **Image Scraping**: Collect images from Telegram channels for object detection.
  - Example Channel: 
    - [Lobelia4cosmetics](https://t.me/lobelia4cosmetics)

#### Steps

- **Python Packages**: Utilize packages such as:
  - `telethon` for Telegram scraping.
  
- **Develop Extraction Scripts**: Write scripts to automate data extraction or use the Telegram application to export content.

- **Storing Raw Data**: 
  - **Initial Storage**: Store raw scraped data in a temporary storage location (local database or files) before further processing.

- **Monitoring and Logging**: 
  - Implement logging to track the scraping process, capture errors, and monitor progress.

### Task 2 - Data Cleaning and Transformation

- **Data Cleaning**: 
  - Remove duplicates.
  - Handle missing values.
  - Standardize formats.
  - Validate data.

- **Storing Cleaned Data**: Store the cleaned data in a database.

- **DBT for Data Transformation**:
  - **Setting Up DBT**: Install DBT (Data Build Tool) and set up a DBT project.
    ```bash
    pip install dbt
    dbt init my_project
    ```
    
  - **Defining Models**: Create DBT models for data transformation. DBT models are SQL files that define transformations on your data.

  - **Run DBT Models**: Execute the DBT models to perform transformations and load data into the data warehouse.
    ```bash
    dbt run
    ```

  - **Testing and Documentation**: Utilize DBT’s testing and documentation features to ensure data quality and provide context for transformations.
    ```bash
    dbt test
    dbt docs generate
    dbt docs serve
    ```

- **Monitoring and Logging**: 
  - Implement logging to track the data cleaning and transformation processes, capture errors, and monitor progress.

### Task 3 - Object Detection

- **Implementing YOLO**: 
  - Utilize the YOLO (You Only Look Once) framework to analyze images collected from Telegram channels.
  
#### Steps

- **Install YOLO Dependencies**: Ensure you have the necessary libraries installed, such as:
  ```bash
  pip install opencv-python
  pip install tensorflow

    Model Training: If required, train the YOLO model on a dataset relevant to Ethiopian medical businesses or use a pre-trained model.

    Image Processing: Write scripts to process images and detect objects, storing results in your database.

    Monitoring and Logging: Implement logging to capture detection results and any errors during processing.

Task 4 - Expose the Collected Data Using FastAPI
Setting Up the Environment

    Install FastAPI and Uvicorn:

    bash

    pip install fastapi uvicorn

Creating a FastAPI Application

    Set up a basic project structure for your FastAPI application:

    bash

    src/
    ├── main.py         # Main entry point for the FastAPI application
    ├── database.py     # Database connection configuration
    ├── models.py       # SQLAlchemy models for database tables
    ├── schemas.py      # Pydantic schemas for data validation
    └── crud.py         # CRUD operations for the database

Description of Each File

    main.py: The main entry point for the FastAPI application, defining the API endpoints.
    database.py: Contains the configuration for the database connection using SQLAlchemy.
    models.py: Defines SQLAlchemy models representing the database tables.
    schemas.py: Contains Pydantic schemas for data validation and serialization.
    crud.py: Implements CRUD (Create, Read, Update, Delete) operations for interacting with the database.

Technologies Used

    Programming Language: Python
    Libraries:
        Telethon (for Telegram API)
        DBT (for data transformation)
        YOLO (for object detection)
        FastAPI (for building APIs)
    Database: Your choice of database (e.g., PostgreSQL, MySQL, SQLite)
    Data Processing Tools: Pandas, NumPy

Installation

To set up the project locally, follow these steps:

    Clone the repository:

    bash

git clone https://github.com/yourusername/ethiopian-medical-data-warehouse.git
cd ethiopian-medical-data-warehouse

Create a virtual environment:

bash

python -m venv .venv

Activate the virtual environment:

    On Windows:

    bash

.venv\Scripts\activate

On macOS/Linux:

bash

    source .venv/bin/activate

Install required packages:

bash

    pip install -r requirements.txt

Contributing

Contributions are welcome! If you have suggestions for improvements or would like to contribute, please fork the repository and submit a pull request.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Instructions for Use

    Adjust any sections as necessary to match your project's details, particularly the GitHub URL in the installation section.
    Add any specific configurations or setup instructions that might be unique to your project.
    Ensure the requirements.txt file is created and includes all necessary packages for installation.
