import cv2
import time
import threading
import pyttsx3
from ultralytics import YOLO
########################################roy_tj#############################################
########################################200205#############################################
# TARGET: Camera 0
CAMERA_ID = 1

# --- CONFIGURATION ---
KNOWN_HEIGHT = 1.7  # Avg object height (meters)
FOCAL_LENGTH = 600  # Camera focal factor
FRAME_WIDTH = 1280  # Resolution Width

# Zone Boundaries
LEFT_LIMIT = FRAME_WIDTH // 3
RIGHT_LIMIT = 2 * (FRAME_WIDTH // 3)

# Urgency Thresholds (Meters)
DIST_VEHICLE_CRITICAL = 5.0  
DIST_OBSTACLE_CRITICAL = 2.0 

# Voice Settings
COOLDOWN = 3.5  # Seconds between sentences

# --- INITIALIZATION ---
engine = pyttsx3.init()
engine.setProperty('rate', 160)
last_speech_time = 0

# Object Categories
VEHICLES = [1, 2, 3, 5, 7] 
OBSTACLES = [0, 56, 57, 60, 67] 

print(f"Loading Intelligent Assistant... (Targeting Camera {CAMERA_ID})")
model = YOLO("yolov8n.pt")

# Pipeline: Native 720p
gst_str = (
    f"nvarguscamerasrc sensor-id={CAMERA_ID} ! "
    "video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=60/1 ! "
    "nvvidconv flip-method=0 ! "
    "video/x-raw, width=1280, height=720, format=BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=BGR ! appsink drop=1"
)

cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
if not cap.isOpened():
    print("Error: Camera failed to open.")
    exit()

# --- HELPER FUNCTIONS ---
def speak(text):
    def _run():
        print(f"Assistant Says: '{text}'") 
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_run).start()

def get_distance(pixel_height):
    if pixel_height == 0: return 0
    return (KNOWN_HEIGHT * FOCAL_LENGTH) / pixel_height

def get_direction(center_x):
    if center_x < LEFT_LIMIT: return "on your Left"
    elif center_x > RIGHT_LIMIT: return "on your Right"
    else: return "in Front of you"

# --- MAIN LOOP ---
print("Assistant Ready. Walking Mode Active.")
prev_time = 0

while True:
    ret, frame = cap.read()
    if not ret: break

    results = model(frame, stream=True)
    highest_priority_msg = None 
    min_dist = 999.0

    for r in results:
        annotated_frame = r.plot()
        if len(r.boxes) > 0:
            boxes = r.boxes.xywh.cpu().numpy()
            classes = r.boxes.cls.cpu().numpy()
            
            for i, box in enumerate(boxes):
                center_x, center_y, width, pixel_height = box
                cls_id = int(classes[i])
                obj_name = model.names[cls_id]
                
                dist = get_distance(pixel_height)
                direction = get_direction(center_x)
                message = None
                
                if cls_id in VEHICLES and dist < DIST_VEHICLE_CRITICAL:
                    color = (0, 0, 255) # Red
                    message = f"Stop! {obj_name} approaching fast!" if direction == "in Front of you" else f"Caution! {obj_name} passing {direction}"
                elif cls_id in OBSTACLES and dist < DIST_OBSTACLE_CRITICAL:
                    color = (0, 255, 255) # Yellow
                    message = f"There is a {obj_name} {direction}"
                else:
                    color = (0, 255, 0) # Green

                label = f"{dist:.1f}m | {direction}"
                x_pos, y_pos = int(center_x - width/2), int(center_y - pixel_height/2)
                cv2.rectangle(annotated_frame, (x_pos, y_pos), (int(x_pos+width), int(y_pos+pixel_height)), color, 2)
                cv2.putText(annotated_frame, label, (x_pos, y_pos-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                if message and dist < min_dist:
                    min_dist = dist
                    highest_priority_msg = message

    current_time = time.time()
    if highest_priority_msg and (current_time - last_speech_time > COOLDOWN):
        speak(highest_priority_msg)
        last_speech_time = current_time

    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Blind Assistant View", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
