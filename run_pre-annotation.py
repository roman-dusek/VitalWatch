import torch
import pandas as pd
from glob import glob
from collections import defaultdict
from transformers import Owlv2Processor, Owlv2ForObjectDetection
from tqdm import tqdm
import numpy as np
from PIL import Image

from transformers.image_utils import ImageFeatureExtractionMixin

mixin = ImageFeatureExtractionMixin()

model_size = "large" # base/large

if model_size =="base":
    processor = Owlv2Processor.from_pretrained("google/owlv2-base-patch16-ensemble")
    model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-base-patch16-ensemble")
elif model_size =="large":
    processor = Owlv2Processor.from_pretrained("google/owlv2-large-patch14-ensemble")
    model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-large-patch14-ensemble")


# Use GPU if available
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

# Set model in evaluation mode
model = model.to(device)
model.eval()

# Text queries to search the image for
text_queries = ["a person lying in bed","a nurse", "an empty bed"]
text_queries = [f"a photo of {i}" for i in text_queries]

# text_queries = ["a person lying in a bed" "a person sitting on a bed", "a nurse","a woman","a men", "a doctor", "an empty bed", "a person in medical clothes", "a person from above", "a person from the back"]
# text_queries = [f"a photo of {i}" for i in text_queries] + ["a detail of a medical device"]

text_inputs = processor(text=text_queries, return_tensors="pt").to(device)

batch_size = 1
score_threshold = 0.30
default_path = "myfiles/videos"
image_paths = glob(default_path+"/**/*.jpg")

detections_dict = defaultdict(list)
previous_detections = pd.read_csv("myfiles/detections.csv")
previous_detections_unique_files = (previous_detections["video_name"]+"/"+previous_detections["file_name"]).unique()


for image_path in tqdm(image_paths):
    video_name, file_name = image_path.rsplit("/",2)[1:]
    if video_name+"/"+file_name in previous_detections_unique_files:
        continue
    image = Image.open(image_path)
    image = Image.fromarray(np.uint8(image)).convert("RGB") 

    # Process image and text inputs
    image_inputs = processor(images=image, return_tensors="pt").to(device)
    image_inputs.update(text_inputs)
    
    # Get predictions
    with torch.no_grad():   
        outputs = model(**image_inputs)
    
    # Load example image
    image_size = model.config.vision_config.image_size
    image = mixin.resize(image, image_size)
    input_image = np.asarray(image).astype(np.float32) / 255.0

    # Get prediction logits
    logits = torch.max(outputs["logits"][0], dim=-1)
    scores = torch.sigmoid(logits.values).cpu().detach().numpy()

    # Get prediction labels and boundary boxes
    labels = logits.indices.cpu().detach().numpy()
    boxes = outputs["pred_boxes"][0].cpu().detach().numpy()
    
    condition = scores > score_threshold
    detections_dict["file_name"].extend([file_name]*condition.sum())
    detections_dict["video_name"].extend([video_name]*condition.sum())
    detections_dict["scores"].extend(scores[condition])
    detections_dict["labels"].extend(labels[condition])
    detections_dict["boxes"].extend([[box] for box in boxes[condition]])

pd.DataFrame(detections_dict).to_csv("detections.csv", index=False)

pd.DataFrame(text_queries).reset_index(names="label_id").to_csv("labels.csv", index=False)
