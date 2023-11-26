Project Title
# Overview
Briefly describe the purpose and goals of the project. Highlight the importance of ICU surveillance event detection and how your solution contributes to better patient monitoring in hospitals.

# Features
List the key features of your project. Include real-time monitoring, YOLO integration, report generation, notification system, and timeline logs.

# Table of Contents
- Installation
- Usage
- Data Annotation Process
- YOLO Integration
- Human-in-the-Loop System
- Reports and Notifications
- Timeline Logs

# Installation
Provide step-by-step instructions on how to install and set up your project. Include any dependencies and system requirements.


```bash
# Copy code
# Example installation steps
git clone https://github.com/yourusername/yourproject.git
cd yourproject
pip install -r requirements.txt

# run annotator in docker-compose
docker-compose up -d --build

# after success instalation open http://0.0.0.0:8080/user/login/
```

# Usage
Explain how to use your project, including starting the surveillance system, monitoring the dashboard, and interpreting the reports.


```bash
Copy code
# Example usage
python main.py
```

# Data Annotation Process
Our data annotation process is split into three parts:
1. Relevant parts of videos are extracted and converted into images for easier manipulation.
2. Pre-annotation of images is done using open-vocabulary model
3. Human annotator approval of pre-annotated images and possible correction of labels
The first part ensures we only make use of relevant parts of videos, which reduces the amount of data we have to process.
In the second part we take advantage of large object detection model to speed up the annotation process, making it also easier for annotators.
The third part ensures that the pre-annotated images are correct and makes corrections where necessary. This process is repeated for all images in the dataset.

# YOLO Integration
Explain how YOLO is integrated into your system, its role in real-time detection, and any customization options.

# Human-in-the-Loop System
Describe the human-in-the-loop system, emphasizing how it enhances the model's accuracy and reliability.

# Reports and Notifications
Highlight the reporting and notification features of your system. Discuss the types of reports generated and the notification mechanisms in place.

# Timeline Logs
Explain how timeline logs are created and their significance in providing a comprehensive overview of events.

# Open source technologies used
- [Owlv2](https://huggingface.co/google/owlv2-large-patch14-ensemble)
- [label-studio](https://labelstud.io/)
- [yolo8](https://github.com/ultralytics/ultralytics)
