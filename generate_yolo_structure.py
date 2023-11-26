import argparse
import pandas as pd
import shutil
import os
import csv
import re

COCO_FOLDER = 'myfiles/yolo-export'
IMAGES_FOLDER = COCO_FOLDER + '/images'
TRAIN_IMAGES = IMAGES_FOLDER + '/train'
TEST_IMAGES = IMAGES_FOLDER + '/val'

LABELS_FOLDER = COCO_FOLDER + '/labels'
TRAIN_LABELS_FOLDER = LABELS_FOLDER + '/train'
TEST_LABELS_FOLDER = LABELS_FOLDER + '/val'


def copy_file(file_path_from: str, file_path_to: str) -> None:
    """Function which copy file path to images"""
    if os.path.exists(file_path_to):
        return
    shutil.copyfile(file_path_from, file_path_to)


def write_annotation(file: str, label, box) -> None:
    """Function which write one annotation into file in txt"""
    with open(file, mode='a', encoding='utf-8') as file:
        file.write(
            "{label} {x} {y} {width} {height}\n".format(label=label, x=box[0], y=box[1], width=box[2], height=box[3]))


def string_to_list(s: str) -> list[float]:
    """Function from string row return array of float"""
    # Use regular expression to find all numbers in the string
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", s)
    return [float(num) for num in numbers[:4]]



def create_output_structure():
    """Function which create output yolo folder"""
    if os.path.exists(COCO_FOLDER):
        shutil.rmtree(COCO_FOLDER)

    os.mkdir(COCO_FOLDER)
    os.mkdir(IMAGES_FOLDER)
    os.mkdir(TRAIN_IMAGES)
    os.mkdir(TEST_IMAGES)

    os.mkdir(LABELS_FOLDER)
    os.mkdir(TRAIN_LABELS_FOLDER)
    os.mkdir(TEST_LABELS_FOLDER)


def generate_yolo_yaml(labels: list[str]):
    """Function generate yolo yaml"""
    with open(COCO_FOLDER + '/' + 'yolo.yaml', mode='w', encoding='utf-8') as file:
        dirname = os.path.dirname(__file__)
        file.write(
            f'path: {dirname}/myfiles/yolo-export\n'
            '\n'
            'train: images/train\n'
            'val: images/val\n'
            '\n'
            'names:\n'
        )
        for index, label in enumerate(labels):
            file.write(f"  {index}: {label}\n")


def generate_yolo(label_file_path: str, detection_file_path: str):
    """Function which generate yolo"""
    create_output_structure()

    labels = []
    with open(label_file_path, mode='r', encoding='utf-8') as label_file:
        reader = csv.DictReader(label_file)
        for row in reader:
            labels.append(re.sub('a photo of an? ', '', row['0']))

    generate_yolo_yaml(labels=labels)

    image_empty_bed = set()
    images_router = {}

    df = pd.read_csv(detection_file_path)
    df.sort_values("labels", ascending=True, inplace=True)

    for index, row in df.iterrows():
        file_name = 'myfiles/images/' + row['video_name'] + '-' + row['file_name']
        coco_file_name_image = row['video_name'] + '-' + row['file_name']
        coco_file_name_txt = coco_file_name_image.replace('.jpg', '.txt')

        label = int(row['labels'])
        box = string_to_list(row['boxes'])

        if label == 0:
            image_empty_bed.add(file_name)

        if label == 2 and (file_name in image_empty_bed):  # if is people lying in the bed and
            continue

        # split train and test data to 80% / 20%
        if not file_name in images_router:
            images_router[file_name] = 'test' if len(images_router.keys()) % 5 == 0 else 'train'

        current_folder = images_router[file_name]
        if current_folder == 'test':
            copy_file(file_path_from=file_name, file_path_to=TEST_IMAGES + '/' + coco_file_name_image)
            write_annotation(file=TEST_LABELS_FOLDER + '/' + coco_file_name_txt, label=label, box=box)
        else:
            copy_file(file_path_from=file_name, file_path_to=TRAIN_IMAGES + '/' + coco_file_name_image)
            write_annotation(file=TRAIN_LABELS_FOLDER + '/' + coco_file_name_txt, label=label, box=box)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Yolo structure creator',
        description='Program generate yolo creating structure'
    )
    parser.add_argument('-l', '--label-file', help='Set the label file', default="myfiles/pre-annotation/labels.csv")
    parser.add_argument('-d', '--detection-file', help='Set the detection file in csv format', default="myfiles/pre-annotation/detections.csv")

    args = parser.parse_args()
    generate_yolo(
        label_file_path=args.label_file,
        detection_file_path=args.detection_file,
    )
