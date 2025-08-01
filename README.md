# Curious Frame

A cool tutor for kids for the Gemma3n Impact Challenge.

## Description

This project is a Python application that acts as a kid tutor to help them interact with the world by capturing what the kid show to the camera using a frame and providing knowledge through speech.

## Getting Started

### Dependencies

* Python 3.8+
* OpenCV
* Ollama

### Installing

```
pip install .
```

### Executing program

```
python src/curious_frame/main.py
```

## Development

Docker start up command:

```
docker run --runtime nvidia --env NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics -it --rm --network host --shm-size=8g --volume /tmp/argus_socket:/tmp/argus_socket --volume /etc/enctune.conf:/etc/enctune.conf --volume /etc/nv_tegra_release:/etc/nv_tegra_release --volume /tmp/nv_jetson_model:/tmp/nv_jetson_model --volume /var/run/dbus:/var/run/dbus --volume /var/run/avahi-daemon/socket:/var/run/avahi-daemon/socket --volume /var/run/docker.sock:/var/run/docker.sock --volume /home/jetorin/projects/jetson-containers/data:/data -v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro --device /dev/snd -e PULSE_SERVER=unix:/run/user/1000/pulse/native -v /run/user/1000/pulse:/run/user/1000/pulse --device /dev/bus/usb --device /dev/video0 --device /dev/video1 --device /dev/i2c-0 --device /dev/i2c-1 --device /dev/i2c-2 --device /dev/i2c-4 --device /dev/i2c-5 --device /dev/i2c-7 --device /dev/i2c-9 --device /dev/ttyACM0 --name jetson_container_20250801_140219 --volume /home/jetorin/curious_frame:/opt/curious_frame --workdir /opt/nanoowl dustynv/nanoowl:r36.4.0
```
