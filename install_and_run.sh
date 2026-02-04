#!/bin/bash

echo "=============================================="
echo "   BLIND ASSIST - AUTO INSTALLER & LAUNCHER   "
echo "=============================================="

# 1. Install System Audio Engine (Espeak) and Pip
echo "[1/4] Installing System Dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip espeak libespeak1 python3-opencv

# 2. Remove "Dumb" OpenCV if it exists (The DLL Hell Fix)
echo "[2/4] Checking for conflicting OpenCV versions..."
if pip3 show opencv-python > /dev/null 2>&1; then
    echo "Removing incompatible pip version of OpenCV..."
    pip3 uninstall -y opencv-python opencv-contrib-python
fi

# 3. Install Python Libraries
echo "[3/4] Installing Python Requirements..."
pip3 install -r requirements.txt

# 4. Launch the Project
echo "[4/4] Setup Complete! Launching Blind Assist..."
python3 run_cam.py
