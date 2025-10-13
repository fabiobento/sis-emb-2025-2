
```bash
sudo apt update
sudo apt upgrade -y
sudo reboot # Reboot to ensure all updates take effect
```


```bash
sudo apt install -y python3-pip python3-venv python3-picamera2
sudo apt install -y libcamera-dev libcamera-tools libcamera-apps
```


```bash
python3 -m venv ~/tflite_env --system-site-packages
```

```bash
source ~/tflite_env/bin/activate
```


```bash
pip install numpy # Numerical processing
pip install pillow  # Image processing
pip install matplotlib  # For displaying images
pip install opencv-python  # Computer vision
```

```bash
pip list | grep -E "(numpy|pillow|opencv|picamera)"
```
