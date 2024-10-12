# scripts/data_transformer.py

import subprocess
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

def run_dbt_models():
    try:
        # Run DBT models to perform transformations
        logging.info("Running DBT models...")
        result = subprocess.run(['dbt', 'run'], check=True, capture_output=True, text=True)
        logging.info("DBT run completed successfully.")
        logging.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during DBT run: {e.stderr}")

def test_dbt_models():
    try:
        # Test DBT models for data quality
        logging.info("Testing DBT models...")
        result = subprocess.run(['dbt', 'test'], check=True, capture_output=True, text=True)
        logging.info("DBT test completed successfully.")
        logging.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during DBT test: {e.stderr}")

def generate_dbt_docs():
    try:
        # Generate DBT documentation
        logging.info("Generating DBT documentation...")
        result = subprocess.run(['dbt', 'docs', 'generate'], check=True, capture_output=True, text=True)
        logging.info("DBT documentation generated successfully.")
        logging.info(result.stdout)

        # Serve the documentation
        logging.info("Serving DBT documentation...")
        subprocess.run(['dbt', 'docs', 'serve'], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during DBT documentation generation: {e.stderr}")

if __name__ == "__main__":
    # Set the environment variable for DBT profile if needed
    os.environ['DBT_PROFILES_DIR'] = r'C:\Users\hayyu.ragea\AppData\Local\Programs\Python\Python312\Ethiopian_Medical_Data\profiles'  # Update this path if necessary

    run_dbt_models()
    test_dbt_models()
    generate_dbt_docs()
