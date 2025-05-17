import cv2
import numpy as np
import time

# Load the pre-trained MobileNet SSD model
def load_model():
    # Load the Caffe model (pre-trained MobileNet SSD)
    net = cv2.dnn.readNetFromCaffe("C:/Users/arb_1/Downloads/deploy.prototxt", "C:/Users/arb_1/Downloads/mobilenet_iter_73000.caffemodel")
    return net

# Function to detect humans
def detect_and_count_humans(frame, net):
    # Prepare the frame for deep learning model
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False)
    
    # Set the input to the model
    net.setInput(blob)
    
    # Forward pass and get the detections
    detections = net.forward()

    # Initialize a counter for detected humans
    count = 0

    # Loop through detections and draw bounding boxes for humans
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:  # Set a threshold for confidence (you can adjust this value)
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            count += 1  # Increment count for each detected human
    
    return frame, count

# Function to save human count to a document
def save_count_to_document(count, timestamp):
    with open("human_count_log.txt", "a") as file:
        file.write(f"{timestamp} - Human Count: {count}\n")

def main():
    # Open webcam
    cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Load pre-trained MobileNet SSD model
    net = load_model()
    
    # Track the time for every 2 minutes
    start_time = time.time()
    
    while True:
        # Capture frame from webcam
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Can't receive frame")
            break
        
        # Resize frame for better performance
        frame = cv2.resize(frame, (640, 480))
        
        # Detect and count humans
        processed_frame, count = detect_and_count_humans(frame, net)
        
        # Display the count
        cv2.putText(
            processed_frame,
            f'People Count: {count}',
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        
        # Display the frame
        cv2.imshow('Human Detection', processed_frame)
        
        # Check if 2 minutes have passed
        elapsed_time = time.time() - start_time
        if elapsed_time >= 120:  # 120 seconds = 2 minutes
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            save_count_to_document(count, timestamp)
            start_time = time.time()  # Reset the start time
        
        # Break loop with 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "_main_":
    main()