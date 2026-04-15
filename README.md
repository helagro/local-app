# Environment Tracker

A program using a sensor hat on a raspberry pi to take and log environmental readings indoors.

## About

Uses a Raspberry Pi B with a Environment Sensor HAT from Waveshare. The code takes readings on set interval or on HTTP requests. The implemented parameters are temperature, humidity, pressure, uv, voc, and light. I use it for taking readings which will be sent to https://exist.io/ (eventually).

## Notes

- Public repository

## Instructions

### Cpp_server

**Build c project manually example:**

```zsh
cmake -S . -B build
cmake --build build
```

**Run dockerfile manually example:**

```zsh
docker run --rm -i -e VAULT=/vault -v $VAULT:/vault cppserv
```


## To Do
