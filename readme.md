# License Plate Detector Project

## Overview

The License Plate Detector Project is a Python-based application for detecting license
plates in videos. This project utilizes computer vision and machine learning techniques
to locate and highlight license plates within video streams.

## Features

- License plate detection in video streams.
- High-accuracy object detection model for locating license plates.
- Support for various video formats.
- Easy-to-use Python script for license plate detection.

### Prerequisites

- Python 3.6 to 3.10.11 version
- Required dependencies (listed in requirements.txt)
- Tesseract setup required (provided in the zip)

# Installation

Step 1: Install virtualenv environment using below command :

    ```pip install virtualenv```

Step 2: Create virtual environment using below command :

    ```python -m venv python_env```

**Note:** python_env is the name of environment,you can give any name in place of python_env.
Create environment inside the license_detector
folder which contains all the project files.

Step 3: Activate the environment using below command :

    ```
        cd license_detector
        python_env\Scripts\activate
    ```

Step 4: Install the Tesseract setup provided in tesseract_setup folder which is present in license_detector folder.

Step 5: Download all the requirments using below command :

    ```pip install -r requirments.txt```

Step 6: You need to provide location of tesseract.exe in extractor_tessaract.py. As shown below.

```
# path to tesseract.exe
 pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\pukhrajsingh\\Desktop\\LicenceModel\\tesseract-ocr\\tesseract.exe'
```

## How to run the app

Run the app.py file which will run the application at localhost:2000. The file we tested for this application is present at `datasets/test.mp4`.

# Acknowledgments

The license plate detection model is based on the YOLO (You Only Look Once) object detection algorithm. Special thanks to the contributors and open-source community for providing valuable libraries and tools.

For any questions or inquiries, please contact any of the contributer.

# Contributors

- Pukhraj Singh (pukharaj.singh@nagarro.com)
- Kartik Mahajan (kartik.mahajan@nagarro.com)
- Anshul Dhawan (anshul.dhawan@nagarro.com)
- Nikhil (nikhil02@nagarro.com)

## Error You might find

You might find the below error while installing required packages :

`The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Cocoa support. If you are on Ubuntu or Debian, install libgtk2.0-dev and pkg-config, then re-run cmake or configure script in function 'cvShowImage' `

To resolve the above error, unisntall opencv_python-headless,opencv-python and install
opencv-python again but not opencv_python-headless.
