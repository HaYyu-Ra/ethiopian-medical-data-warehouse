import logging
import os

def setup_logging(log_dir='logs', log_file='yolo_object_detection.log'):
    """Sets up logging configuration."""

    # Create log directory if it does not exist
    os.makedirs(log_dir, exist_ok=True)

    # Define log file path
    log_file_path = os.path.join(log_dir, log_file)

    # Create a logging format
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level to DEBUG
        format=logging_format,
        handlers=[
            logging.FileHandler(log_file_path),  # Log to a file
            logging.StreamHandler()               # Also log to console
        ]
    )

    # Log that logging is set up
    logging.info("Logging is set up successfully. Log file: %s", log_file_path)

# Call the setup_logging function if this script is executed
if __name__ == "__main__":
    setup_logging()
