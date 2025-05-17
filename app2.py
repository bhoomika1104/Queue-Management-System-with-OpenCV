from flask import Flask, request, render_template, jsonify
import cv2
import numpy as np
import base64
import os

app = Flask(__name__)

# Specify the path to your model files
model_dir = 'E:/nimith/model_files'

# Load the pre-trained MobileNetSSD model (Caffe version) using the path to the model files
net = cv2.dnn.readNetFromCaffe(
    os.path.join(model_dir, r'deploy.prototxt'),  # Path to Caffe model configuration
    os.path.join(model_dir, r'mobilenet_iter_73000.caffemodel')  # Path to pre-trained model weights
)

# List of classes that MobileNetSSD detects
class_names = ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow',
               'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

def detect_people(image_bytes):
    """Detect the number of humans in the image using MobileNetSSD deep learning model."""
    # Convert byte data to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Resize the image to 300x300 (MobileNetSSD input size)
    img_resized = cv2.resize(img, (300, 300))

    # Prepare the image for the model (mean subtraction and scaling)
    blob = cv2.dnn.blobFromImage(img_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), swapRB=False)

    net.setInput(blob)

    # Perform detection
    detections = net.forward()

    # Count the number of people detected
    people_count = 0
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.1:  # Confidence threshold to filter weak detections
            class_id = int(detections[0, 0, i, 1])
            if class_names[class_id] == 'person':
                people_count += 1

    return people_count

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/employee')
def employee():
    customers = [{"token": 1234, "name": "John Doe", "counter": "1", "batch": "1", "status": "In Process"}]
    return render_template('employee.html', customers=customers)

@app.route('/customer')
def customer():
    return render_template('customer.html')

@app.route('/capture_image', methods=['POST'])
def capture_image():
    """Receive the image captured from the webcam and detect humans."""
    image_data = request.json['image']  # Assuming the image data is in base64 format
    
    # Decode base64 to bytes
    image_bytes = base64.b64decode(image_data.split(',')[1])  # Remove 'data:image/png;base64,' part

    # Detect people in the image
    number_of_people = detect_people(image_bytes)

    # Return the number of people detected as JSON
    return jsonify({"people_detected": number_of_people})

if __name__ == '__main__':
    app.run(debug=True)
