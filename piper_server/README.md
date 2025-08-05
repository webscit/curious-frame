# Piper server for the curious frame

## Build the docker

```
docker build --tag piper-jetson .
```

## Execute the docker

```
docker run --runtime nvidia --env NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics --shm-size=8g --network host --rm piper-jetson
```
