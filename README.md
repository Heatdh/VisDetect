# Rapeseed Detection and Spray Painting Robot

This repository contains the software for a robot that detects specific shapes and colors to simulate the detection of male rapeseed plants. The robot moves towards the detected plants and controls a nozzle to spray paint them. The software is divided into three modules: control, vision, and motion. The software is designed to be deployed on an NVIDIA Jetson platform.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Detect specific shapes and colors representing male rapeseed plants using computer vision algorithms.
- Control the robot's motion towards the detected plants.
- Operate a spray nozzle to paint the detected plants.
- Coordinate between control, vision, and motion modules to perform the task.
- Deploy on NVIDIA Jetson platform for real-time processing.

## Requirements

- Python 3.6 or higher
- OpenCV 4.x
- NumPy
- NVIDIA Jetson platform (for deployment)

## Installation

1. Clone the repository to your local machine or Jetson device:

```bash
git clone https://github.com/yourusername/rapeseed-detection-robot.git
```

2. download requirements a requirements.txt will be provided by the end of the project