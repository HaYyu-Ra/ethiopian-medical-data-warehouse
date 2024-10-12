import cv2
import os
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define paths to YOLO config and weights
weights_path = "C:\\Users\\hayyu.ragea\\AppData\\Local\\Programs\\Python\\Python312\\Ethiopian_Medical_Data\\scripts\\object_detection\\yolov3.weights"
config_path = "C:\\Users\\hayyu.ragea\\AppData\\Local\\Programs\\Python\\Python312\\Ethiopian_Medical_Data\\scripts\\object_detection\\yolov3.cfg"

# Load YOLO
try:
    # Check if the weight and config files exist
    if not os.path.isfile(weights_path):
        logging.error(f"Weights file not found: {weights_path}")
        raise FileNotFoundError(weights_path)

    if not os.path.isfile(config_path):
        logging.error(f"Config file not found: {config_path}")
        raise FileNotFoundError(config_path)

    # Load YOLO model
    net = cv2.dnn.readNet(weights_path, config_path)
    layer_names = net.getLayerNames()
    output_layers_indices = net.getUnconnectedOutLayers()  # This returns indices directly.
    output_layers = [layer_names[i - 1] for i in output_layers_indices]  # Adjust for 1-based indexing
    logging.info("YOLO model loaded successfully.")

except Exception as e:
    logging.error(f"Error loading YOLO model: {e}")
    raise

def detect_objects(image_path):
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            logging.error(f"Image not found at path: {image_path}")
            return [], None  # Always return a tuple

        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Processing the outputs (for example, bounding boxes)
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:  # Confidence threshold
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    boxes.append([center_x, center_y, w, h])
        
        logging.info(f"Detected boxes: {boxes}")
        return boxes, img  # Always return boxes and img

    except Exception as e:
        logging.error(f"Error in object detection: {e}")
        return [], None  # Return empty list and None for img

def save_detected_image(original_image, boxes, output_path):
    # Draw bounding boxes on the image
    for box in boxes:
        x, y, w, h = box
        cv2.rectangle(original_image, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (0, 255, 0), 2)

    # Save the image with detected boxes
    cv2.imwrite(output_path, original_image)
    logging.info(f"Saved detected image to: {output_path}")

# Define the directory containing images
image_directory = r'C:\Users\hayyu.ragea\AppData\Local\Programs\Python\Python312\Ethiopian_Medical_Data\data\raw\telegram_data'

# Define the directory to save detected images
output_directory = r'C:\Users\hayyu.ragea\AppData\Local\Programs\Python\Python312\Ethiopian_Medical_Data\data\detected_images'

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Process all images in the specified directory
for filename in os.listdir(image_directory):
    if filename.endswith(('.jpg', '.jpeg', '.png')):  # Add other formats as needed
        image_path = os.path.join(image_directory, filename)
        
        # Check if the image file exists before processing
        if not os.path.isfile(image_path):
            logging.error(f"Image not found at path: {image_path}")
            continue
        
        detected_boxes, original_image = detect_objects(image_path)

        if detected_boxes and original_image is not None:
            logging.info(f"Detected boxes for {filename}: {detected_boxes}")
            # Save the image with detected boxes
            output_path = os.path.join(output_directory, filename)  # Save with the same name
            save_detected_image(original_image, detected_boxes, output_path)
        else:
            logging.info(f"No boxes detected for {filename} or image could not be read.")
