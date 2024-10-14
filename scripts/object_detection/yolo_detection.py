import torch
import cv2
import numpy as np
import os
import logging
import psycopg2
from psycopg2 import sql

# Set up logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("yolo_detection.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)

class YOLOModel:
    def __init__(self, weights_path, labels_path):
        # Verify file paths
        if not os.path.isfile(weights_path):
            logging.error(f"File not found: {weights_path}")
            raise FileNotFoundError(f"File not found: {weights_path}")

        # Load YOLOv5 model
        logging.info("Loading YOLO model...")
        try:
            self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path)
            logging.info("YOLO model loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load YOLO model: {e}")
            raise

        # Load COCO labels
        if not os.path.isfile(labels_path):
            logging.error(f"Labels file not found: {labels_path}")
            raise FileNotFoundError(f"Labels file not found: {labels_path}")

        with open(labels_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        logging.info(f"Loaded {len(self.classes)} classes.")

    def detect_objects(self, image, confidence_threshold=0.25):
        """Perform object detection on the image."""
        logging.info("Performing object detection...")
        results = self.model(image)  # Run inference
        detections = []

        # Parse results
        for *xyxy, conf, cls in results.xyxy[0]:
            if conf < confidence_threshold:  # Filter based on confidence
                continue
            
            x1, y1, x2, y2 = map(int, xyxy)  # Get bounding box coordinates
            class_id = int(cls)  # Use class_id instead of label
            confidence = float(conf)

            detections.append({
                'class_id': class_id,
                'confidence': confidence,
                'box': [x1, y1, x2 - x1, y2 - y1]  # box format: [x, y, width, height]
            })

        if not detections:
            logging.warning("No valid detections found.")
        else:
            logging.info(f"Detections found: {len(detections)}")
        
        return detections

    def draw_boxes(self, image, detections):
        """Draw detection boxes on the image."""
        for detection in detections:
            x, y, w, h = detection['box']
            class_id = detection['class_id']
            confidence = detection['confidence']
            label = self.classes[class_id]  # Get the label using class_id
            
            # Draw the bounding box
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = f"{label}: {confidence:.2f}"
            
            # Put label text
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

def insert_detections_to_db(detections, filename):
    """Insert detection results into the PostgreSQL database."""
    connection = None
    cursor = None
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname="Object_detection",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        # Insert detection data into the Image_detection table
        insert_query = sql.SQL("INSERT INTO Image_detection (filename, class_id, confidence, x_min, y_min, width, height) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        
        for detection in detections:
            cursor.execute(insert_query, (
                filename,
                detection['class_id'],  # Use class_id directly
                detection['confidence'],
                detection['box'][0],  # x_min
                detection['box'][1],  # y_min
                detection['box'][2],  # width
                detection['box'][3]   # height
            ))

        # Commit changes
        connection.commit()
        logging.info("Detections inserted into the Image_detection table successfully.")
        
    except Exception as e:
        logging.error(f"Database error: {e}")
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            logging.info("Database connection closed.")

def process_images(input_folder, output_folder, yolo, summary_txt_path):
    """Process all images in the input folder and save the detections in the output folder."""
    # Check if input folder exists, create if not
    os.makedirs(input_folder, exist_ok=True)

    # Check if output folder exists, create if not
    os.makedirs(output_folder, exist_ok=True)

    # Create a summary text file for all detections
    with open(summary_txt_path, 'w') as summary_file:
        # Iterate over each image in the input folder
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                image_path = os.path.join(input_folder, filename)
                logging.info(f"Processing image: {image_path}")

                # Load image
                image = cv2.imread(image_path)
                if image is None:
                    logging.warning(f"Could not read image: {image_path}. Skipping.")
                    continue

                # Perform object detection
                detections = yolo.detect_objects(image)

                # Draw boxes on the image
                yolo.draw_boxes(image, detections)

                # Save the output image
                output_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_path, image)
                logging.info(f"Detected image saved to: {output_path}")

                # Save labeled names to the summary text file
                if detections:
                    for detection in detections:
                        class_id = detection['class_id']
                        confidence = detection['confidence']
                        box = detection['box']
                        label = yolo.classes[class_id]  # Get label from class_id
                        summary_file.write(f"{filename}: {label} {confidence:.2f} {box[0]} {box[1]} {box[2]} {box[3]}\n")
                else:
                    # If no detections, record that no objects were found
                    summary_file.write(f"{filename}: No detections found\n")
                    logging.info(f"No detections for {filename}.")

                logging.info(f"Detection results for {filename} saved to the summary file.")
                
                # Insert detections into the database
                insert_detections_to_db(detections, filename)

if __name__ == "__main__":
    # Replace these with the correct file paths
    weights_path = "C:/Users/hayyu.ragea/AppData/Local/Programs/Python/Python312/Ethiopian_Medical_Data/yolov5/yolov5s.pt"
    labels_path = "C:/Users/hayyu.ragea/AppData/Local/Programs/Python/Python312/Ethiopian_Medical_Data/yolov5/coco.names"
    input_folder = "C:/Users/hayyu.ragea/AppData/Local/Programs/Python/Python312/Ethiopian_Medical_Data/data/telegram_data"  # Updated path
    output_folder = "C:/Users/hayyu.ragea/AppData/Local/Programs/Python/Python312/Ethiopian_Medical_Data/output_images"
    summary_txt_path = "C:/Users/hayyu.ragea/AppData/Local/Programs/Python/Python312/Ethiopian_Medical_Data/detection_summary.txt"

    # Initialize YOLO model
    try:
        yolo_model = YOLOModel(weights_path, labels_path)
        # Process the images
        process_images(input_folder, output_folder, yolo_model, summary_txt_path)
    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
