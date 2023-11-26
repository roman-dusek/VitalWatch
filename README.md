Project Title
# Overview
The ICU Surveillance Event Detection System is an innovative solution designed to revolutionize patient monitoring within hospital intensive care units. Leveraging state-of-the-art technologies such as YOLO (You Only Look Once) for real-time object detection, this system provides a comprehensive and adaptive approach to capturing and annotating critical events during shifts.

# Key Features
Real-time Monitoring: Utilizing YOLO for object detection, the system ensures immediate and accurate identification of events within ICU rooms.

Human-in-the-Loop System: The integration of a human-in-the-loop system enhances model accuracy and adaptability through continuous annotator approvals, creating a dynamic and self-improving surveillance system.

Open-Vocabulary Model: Pre-annotation with an open-vocabulary model allows for the identification of classes not initially trained, ensuring adaptability to emerging scenarios and classes.

# Table of Contents
- Installation
- Usage
- Data Annotation Process
- YOLO Integration
- Human-in-the-Loop System
- Reports and Notifications
- Timeline Logs

# Installation

```bash
# after cloning repo, install dependencies
make install_local
```

# Usage
Explain how to use your project, including starting the surveillance system, monitoring the dashboard, and interpreting the reports.
We have made are project as simple as possible to use. All of the stages of our systems are called by make commands.

```bash
# clipp videos into interesting videos/frames to be annotated
make clip_videos
# script expects videos to be in myfiles/raw_videos folder
# script will create myfiles/images folder and put clipped videos there
# you can also choose export of short clips that can be also anotated for object tracking
```

```bash
# pre-annotate images using open-vocabulary model
make run_pre-annotation
```

```bash
# pre-annotate images using open-vocabulary model
make start_labelstudio
```

```bash
# finetuned pretrained yolo for ICU use case
make train_yolo
```


# Data Annotation Process

Our data annotation process unfolds in three distinct phases:

1. Video Segmentation: We initiate by extracting pertinent segments from videos, converting them into images for streamlined handling. This strategic approach ensures that only relevant portions of videos are utilized, thereby minimizing the data processing workload.

2. Open-Vocabulary Pre-Annotation: In the subsequent step, we employ an open-vocabulary model for pre-annotation of images. This model, designed for large-scale object detection, significantly accelerates the annotation process. Its expansive capabilities enhance the efficiency of annotators by providing a head start in labeling diverse objects within the images.

3. Human-Annotator Validation: The final phase involves human annotators reviewing and approving the pre-annotated images. This step serves a dual purpose: validating the accuracy of pre-annotations and allowing for any necessary corrections. This iterative process ensures that the dataset is meticulously curated, with human expertise refining the model's annotations. This cycle is systematically applied to all images in the dataset.

This multi-phase approach not only streamlines the annotation workflow but also guarantees the accuracy and relevance of annotations through a collaborative effort between automated processes and human validation.

# YOLO Integration
The integration of YOLO (You Only Look Once) into the ICU Surveillance Event Detection System plays a pivotal role in achieving real-time and accurate object detection within hospital intensive care units. YOLO is a state-of-the-art deep learning algorithm that excels at detecting and classifying objects in images or video frames swiftly and with high precision.

# Human-in-the-Loop System
The Human-in-the-Loop (HITL) system integrated into the ICU Surveillance Event Detection plays a crucial role in enhancing the accuracy, reliability, and adaptability of the overall model. By actively involving human annotators in the loop, this system ensures continuous learning and refinement, addressing the inherent challenges of real-world scenarios and maintaining a high standard of precision in event detection.

![hil.png](images%2Fhil.png)

# Reports and Notifications
One of our vision is to provide a real-time monitoring system for ICU patients. This can be easily achieved by uring YOLO to detect the patient's movement and send notification based on some dangerous events being detected to the medical staff.
To achieve this, we have implemented a notification system that alerts the medical staff when a patient is in need of attention.
Tha can be achieved both  by sending notification to main dashboard or sending notification to mobile device.

# Timeline Logs

![timelog.png](images%2Ftimelog.png)

# Next Steps
List the next steps for your project, including additional features and improvements.
- [ ] automating pipeline to be able to run on locally inside IKEM
- [ ] schedulling jobs using airflow

# Open source technologies used
- [Owlv2](https://huggingface.co/google/owlv2-large-patch14-ensemble)
- [label-studio](https://labelstud.io/)
- [yolo8](https://github.com/ultralytics/ultralytics)
