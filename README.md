# Blind Assist Project: Portable Vision Assistant

**Author:** Turjo Roy  
**Device:** Nvidia Jetson Orin Nano 8GB (2025 Model)  
**Status:** Prototype (V0.0.1)

## 📖 Project Overview
The **Blind Assist Project** is an offline, edge-AI wearable device designed to assist visually impaired individuals in navigating the real world. By leveraging the power of the **Nvidia Jetson Orin Nano**, this system performs real-time object detection and distance estimation without relying on cloud connectivity, ensuring low latency and reliability in outdoor environments.

This repository contains the source code for the standalone portable version of the system.

## ✨ Key Features
* **Real-Time Object Detection:** Utilizes the **YOLOv8** (Nano) architecture optimized for the Jetson GPU to identify obstacles (people, vehicles, furniture, etc.).
* **Distance Estimation:** Custom algorithm estimates the proximity of detected objects to warn the user of immediate collisions.
* **Edge Computing:** Runs entirely locally on the Jetson Orin Nano, requiring no internet connection.
* **Portable Deployment:** Designed to be battery-operated and wearable.

## 🛠️ Hardware Requirements
* **Nvidia Jetson Orin Nano 8GB** (Developer Kit)
* **USB Camera / CSI Camera** (Project currently configured for single-camera input, e.g., right-eye stereo feed)
* **Power Bank** (5V/3A minimum for portable usage)
* **Audio Output** (Headphones or Mini-Speaker for alerts - *In Progress*)

## ⚙️ Software Dependencies
* **JetPack 6.x** (Ubuntu 22.04)
* **Python 3.8+**
* **Ultralytics YOLO**
* **PyTorch** (with CUDA support for Jetson)
* **OpenCV**

## 🚀 Installation & Setup

### 1. Clone the Repository
Open your terminal on the Jetson Nano and run:
```bash
git clone [https://github.com/tj2002roy/Blind-Assist_Project_V0.0.1.git](https://github.com/tj2002roy/Blind-Assist_Project_V0.0.1.git)
cd Blind-Assist_Project_V0.0.1
```
#2. Install Dependencies
We have provided a requirements.txt file to install necessary Python libraries.

```Bash
pip3 install -r requirements.txt
Note: Ensure you have the correct version of PyTorch installed for your JetPack version before installing Ultralytics.
```
3. Setup Permissions
If you plan to use the automated shell script, make it executable:

```Bash
chmod +x install_and_run.sh
```
🏃 Usage
Option 1: Quick Start (Shell Script)
Run the automated script to setup the environment and launch the camera:

```Bash
./install_and_run.sh
```
Option 2: Manual Run
To run the main detection script directly with Python:

```Bash
python3 run_cam.py
```
🧠 Methodology
Input: Video frames are captured via cv2 from the attached camera.

Inference: Frames are passed to the yolov8n.pt model loaded on the GPU (CUDA).

Processing: * The model returns bounding boxes and class IDs.

The system calculates the center point of the box.

Distance Logic: Distance is estimated based on the relative size of the bounding box compared to the frame reference.

Output: Visual overlay (for debugging) and audio/haptic signals (for the user).

🔮 Future Roadmap
[ ] Integration of depth-sensing cameras (Stereo/Intel RealSense) for higher precision.

[ ] Text-to-Speech (TTS) engine integration for describing the scene to the user.

[ ] Optimization of battery life for extended outdoor use.

[ ] "Find My Object" voice command feature.

⚠️ Important Notes
Model Weights: The repository includes yolov8n.pt. If you train a custom model, replace this file and update the path in run_cam.py.

Camera Index: If run_cam.py fails to open the camera, check the video index (usually 0 or 1) in the source code: cap = cv2.VideoCapture(0).

📄 License
This project is open for research and educational purposes.


### **How to Add This to Your Repo:**
1.  Create the file in your terminal:
    ```bash
    nano README.md
    ```
2.  **Paste** the text above into the file.
3.  Press **Ctrl+O**, then **Enter** to save.
4.  Press **Ctrl+X** to exit.
5.  Upload it:
    ```bash
    git add README.md
    git commit -m "Added Project README"
    git push
    ```
