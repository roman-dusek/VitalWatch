# Overview
The ICU Surveillance Event Detection System is an innovative solution designed to revolutionize patient monitoring within hospital intensive care units. Leveraging state-of-the-art technologies such as YOLO (You Only Look Once) for real-time object detection, this system provides a comprehensive and adaptive approach to annotating and capturing critical events during shifts.

# Key Features
**Open-Vocabulary Model**: Pre-annotation with an open-vocabulary model allows for the identification of classes not initially trained, ensuring adaptability to emerging scenarios and classes.

**Human-in-the-Loop System**: The integration of a human-in-the-loop system enhances model accuracy and adaptability through continuous annotating, creating a dynamic and self-improving surveillance system.

**Real-time Monitoring**: Utilizing YOLO for object detection, the system ensures immediate and accurate identification of events within ICU rooms.

# Data Annotation Process

Data annotation process, the pinnacle of our system, unfolds in three distinct phases:

1. **Video Segmentation**: We initiate by extracting segments from videos, converting them into images for streamlined handling. **This strategic approach ensures that only relevant portions of videos are utilized, thereby minimizing the data processing workload.**

2. Open-Vocabulary **Pre-Annotation**: In the subsequent step, we employ an open-vocabulary model for pre-annotation of images. This model, designed for large-scale object detection, **significantly accelerates the annotation process. Its expansive capabilities enhance the efficiency of annotators by providing a head start in labeling diverse objects within the images.**

3. **Human-Annotator Validation**: The final phase involves human annotators reviewing and improving the pre-annotated images. **This step serves a dual purpose: validating the accuracy of pre-annotations and allowing for any necessary corrections. This iterative process ensures that the dataset is curated, with human expertise refining the model's annotations. This cycle is systematically applied to all images in the dataset.**

This multi-phase approach not only streamlines the annotation workflow but also guarantees the accuracy and relevance of annotations through a collaborative effort between automated processes and human validation.

![hil.png](images%2Fhil.png)

# Frontend in Label Studio
![img.png](images%2Fimg.png)

# YOLO Integration
The integration of YOLO into the ICU Surveillance Event Detection System plays a pivotal role in achieving real-time and accurate object detection within hospital intensive care units. YOLO is a state-of-the-art deep learning algorithm that excels at detecting and classifying objects in images or video frames swiftly and with high precision.

## YOLO Training Process
In the root folder, there's a Python notebook named `Train_YOLOv8.ipynb`, which details the YOLO training process.

## Experimental Training of YOLO v8
For the experimental training phase, YOLO v8 was employed. The training set comprised 400 images, while the validation set included 100 images. The process and outcomes of the training are meticulously documented in the final statistics, as shown in the image.
![yolo-training-results.png](images%2Fyolo-training-results.png)
After extensive training, the most effective model weights were identified and are now stored in `weights/best.pt`.

## Further Development and Optimization
Moving forward, our focus will shift towards further optimization of the YOLO model to enhance its accuracy and efficiency in real-world ICU scenarios. This will include tweaking the model parameters, experimenting with different training datasets, and potentially integrating additional layers or features to improve object detection under various conditions typical of intensive care environments.
In root folder is located python notebok which name `Train_YOLOv8.ipynb` with describing yolo training process.

# Installation

```bash
# after cloning repo, install dependencies
make install_local
```

For usage yolo trained model with weight, is need clone repo by this command

```bash
git lfs clone git@github.com:roman-dusek/VitalWatch.git
```

# Usage
We have made are project as simple as possible to use. All of the stages of our systems are called by make commands.

```bash
# clipp videos into interesting videos/frames to be annotated
make clip_videos
# script expects videos to be in myfiles/raw_videos folder
# script will create myfiles/images folder and put clipped videos there
# you can also choose export of short clips that can be also anotated for object tracking
> Clipping videos has finished.
> Clipped 12 videos, in total 8 hours of video.
> Prepared 554 interval for pre-annotation, in total 2 hours of video.
```

```bash
# pre-annotate images using open-vocabulary model
make run_pre-annotation
> Pre-annotation has finished
> Recognizing 1873 objects in 554 intervals.
```

```bash
# pre-annotate images using open-vocabulary model
make start_labelstudio
```

```bash
# generate images from video in interesting parts, default store folder is myfiles/images
python video_frame_generator.py --file-name=video.avi --time-window=20 --threshold=700 --save-path=myfiles/images
```

```bash
# generate yolo-export training structure which is ready for training. It's locate in myfiles/yolo-export folder
python generate_yolo_structure --label-file=/myfiles/pre-annotation/labels.csv --detection-file=myfiles/pre-annotation/detections.csv
```

# Reports and Notifications
One of our vision is to provide a real-time monitoring system for ICU patients. This can be easily achieved by uring YOLO to detect the patient's movement and send notification based on some dangerous events being detected to the medical staff.
To achieve this, we have implemented a notification system that alerts the medical staff when a patient is in need of attention.
Tha can be achieved both  by sending notification to main dashboard or sending notification to mobile device.

# Timeline Logs
example for ilustration purposes

![timelog.png](images%2Ftimelog.png)

# Next Steps
List the next steps for your project, including additional features and improvements.
- [ ] automating pipeline to be able to run on locally inside IKEM
- [ ] schedulling jobs using airflow

# Open source technologies used
- [Owlv2](https://huggingface.co/google/owlv2-large-patch14-ensemble)
- [label-studio](https://labelstud.io/)
- [yolo8](https://github.com/ultralytics/ultralytics)
