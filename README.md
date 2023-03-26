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

## Usage

1. Ensure the robot and camera hardware are connected and configured properly.
2. Run the main script to start the rapeseed detection and spray painting process:


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

git clone https://github.com/yourusername/rapeseed-detection-robot.git


2. Change to the repository's directory:

cd rapeseed-detection-robot


3. (Optional) Create a virtual environment for the project:

python3 -m venv venv
source venv/bin/activate



4. Install the required Python packages:

pip install -r requirements.txt


## Usage

1. Ensure the robot and camera hardware are connected and configured properly.
2. Run the main script to start the rapeseed detection and spray painting process:

python main.py

3. Monitor the robot's progress and adjust parameters as needed.

## Contributing

Contributions to this project are welcome. To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch with a descriptive name.
3. Commit your changes to the branch.
4. Create a pull request describing the changes you've made.

Please ensure your code follows the project's style guidelines and passes all tests.


## License

This project is licensed under the [MIT License](LICENSE). Please refer to the `LICENSE` file for more information.