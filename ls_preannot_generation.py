import pandas as pd
import json

df = pd.read_csv("myfiles/pre-annotation/detections.csv")

labels_mapping = pd.read_csv("myfiles/pre-annotation/labels.csv")
labels_mapping = dict(labels_mapping.values)


def convert_absolute_to_relative(cx, cy, w, h, image_width=1280, image_height=960):
    cx_rel = cx / image_width
    cy_rel = cy / image_height
    w_rel = w / image_width
    h_rel = h / image_height
    return cx_rel, cy_rel, w_rel, h_rel


def convert_relative_to_absolute(cx_rel, cy_rel, w_rel, h_rel, image_width=1280, image_height=960):
    cx = cx_rel * image_width
    cy = cy_rel * image_height
    w = w_rel * image_width
    h = h_rel * image_height
    return cx, cy, w, h


def convert_center_to_corner(cx, cy, w, h):
    x0 = cx - (w / 2)
    y0 = cy - (h / 2)
    return x0, y0, w, h


def convert_boxes(cx, cy, w, h, width=1280, height=960):
    cx_rel, cy_rel, w_rel, h_rel = convert_relative_to_absolute(cx, cy, w, h, width, height)
    cx, cy, w, h = convert_center_to_corner(cx_rel, cy_rel, w_rel, h_rel)
    return convert_absolute_to_relative(cx, cy, w, h)


label_studio_data =[]
count = 1
for (video_name, file_name), df_rows in df.groupby(["video_name", "file_name"])[["scores","labels","boxes"]]:
    image_url = f"/data/local-files/?d=images/{video_name}-{file_name}"

    results = []
    for i, row in df_rows.iterrows():
        boxes = eval(row.boxes.split("(",1)[1].rsplit(",",1)[0])
        x0, y0, w, h = convert_boxes(*boxes)
        if row["labels"] == 2:
            continue

        results.append({
            "id": f"result{count}",
            "type": "rectanglelabels",
            "from_name": "label",
            "to_name": "image",
            "original_width": 1280,
            "original_height": 960,
            "image_rotation": 0,
            "value": {
                "rotation": 0,
                "x": x0*100,  # Adjust these according to your actual column names
                "y": y0*100,
                "width": w*100,
                "height": h*100,
                "rectanglelabels": [labels_mapping[row["labels"]]]  # Replace with your actual label from label_id
            }
        })
        count+=1

    # Create the Label Studio JSON structure for each row
    label_studio_row = {
        "data": {
            "image": image_url
        },
        "predictions": [{
            "model_version": "v1",
            "score": 0.5,
            "result": results
        }]
    }
    # Append the current row's Label Studio data to the list
    label_studio_data.append(label_studio_row)

# Convert the list to JSON
label_studio_json = json.dumps(label_studio_data, indent=2)

# Save the JSON data to a file
with open('label_studio_data.json', 'w') as file:
    file.write(label_studio_json)
