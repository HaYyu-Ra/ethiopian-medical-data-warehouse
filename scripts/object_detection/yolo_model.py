import cv2
import numpy as np
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class YOLOModel:
    def __init__(self, weights_path, config_path, labels_path):
        # Verify file paths
        for path in [weights_path, config_path, labels_path]:
            if not os.path.isfile(path):
                logging.error(f"File not found: {path}")
                raise FileNotFoundError(f"File not found: {path}")
        
        # Load YOLO network
        logging.info("Loading YOLO model...")
        self.net = cv2.dnn.readNet(weights_path, config_path)
        logging.info("YOLO model loaded successfully.")
        
        # Load COCO labels
        with open(labels_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        # Get output layer names
        self.layer_names = self.net.getLayerNames()
        try:
            unconnected_layers = self.net.getUnconnectedOutLayers()
            self.output_layers = [self.layer_names[i - 1] for i in unconnected_layers.flatten()]
        except Exception as e:
            logging.error(f"Error in processing output layers: {e}")
            raise
        logging.info("Model initialized with output layers and labels.")

    def detect_objects(self, image):
        """Perform object detection on the image."""
        height, width, _ = image.shape
        
        # Prepare image for YOLO
        logging.info("Preparing image for YOLO detection.")
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        
        # Perform forward pass
        logging.info("Running forward pass for object detection.")
        layer_outputs = self.net.forward(self.output_layers)
        
        # Initialize detection lists
        boxes, confidences, class_ids = [], [], []
        
        # Iterate through each output
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                # Filter detections by confidence
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        # Apply Non-Maximum Suppression (NMS) to remove redundant overlapping boxes
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)
        
        detections = []
        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                confidence = confidences[i]
                detections.append({
                    'label': label,
                    'confidence': confidence,
                    'box': [x, y, w, h]
                })
        
        return detections

    def draw_boxes(self, image, detections):
        """Draw detection boxes on the image."""
        for detection in detections:
            x, y, w, h = detection['box']
            label = detection['label']
            confidence = detection['confidence']
            
            # Draw the bounding box
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = f"{label}: {confidence:.2f}"
            
            # Put label text
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

def process_images(input_folder, output_folder, yolo):
    """Process all images in the input folder and save the detections in the output folder."""
    # Check if output folder exists, create if not
    os.makedirs(output_folder, exist_ok=True)

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

if __name__ == "__main__":
    # Replace these with the correct file paths
    weights_path = "C:/Users/hayyu.ragea/AppData/Local/Programs/Python/Python312/Ethiopian_Medical_Data/scripts/object_detection/yolov3.weights"
    config_path = "C:/Users/hayyu.ragea/AppData/Local/Programs/Python/Python312/Ethiopian_Medical_Data/scripts/object_detection/yolov3.cfg"
    labels_path = "C:/Users/hayyu.ragea/AppData/Local/Programs/Python/Python312/Ethiopian_Medical_Data/scripts/object_detection/coco.names"

    # Input and output folder paths
    input_folder = "C:/Users/hayyu.ragea/AppData/Local/Programs/Python/Python312/Ethiopian_Medical_Data/data/raw/telegram_data"
    output_folder = "C:/Users/hayyu.ragea/AppData/Local/Programs/Python/Python312/Ethiopian_Medical_Data/data/detected_images"

    # Initialize the YOLO model
    yolo = YOLOModel(weights_path, config_path, labels_path)

    # Process all images in the input folder
    process_images(input_folder, output_folder, yolo)

    logging.info("Processing complete.")
