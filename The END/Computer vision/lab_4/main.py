import os
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import ToTensor
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tqdm import tqdm  # Import tqdm for progress bars

# === SETTINGS ===
BASE_DIR = "df"
LABEL_TYPE = "human"  # "human" or "machine"
SPLIT = "validation"  # "train" or "validation"
USE_THUMBNAILS = True  # Use Thumbnail300KURL if True, OriginalURL if False
SELECTED_CLASSES = ["/m/01cbzq", "/m/03g3w"]  # Edit based on your classes of interest
label_map = {"/m/01cbzq": 1, "/m/03g3w": 2}  # Map /m/... to class indices starting from 1

# === LOAD METADATA & LABELS ===
images_csv = pd.read_csv(f"{BASE_DIR}/images/{SPLIT}/images.csv")
labels_csv = pd.read_csv(f"{BASE_DIR}/{LABEL_TYPE}/{SPLIT}/labels.csv")
labels_csv = labels_csv[labels_csv['LabelName'].isin(SELECTED_CLASSES)]
image_ids = labels_csv['ImageID'].unique()
images_csv = images_csv[images_csv['ImageID'].isin(image_ids)]
url_map = dict(zip(images_csv['ImageID'], images_csv['Thumbnail300KURL' if USE_THUMBNAILS else 'OriginalURL']))

# === DATASET ===
class OpenImagesDataset(Dataset):
    def __init__(self, labels_df, url_map, label_map, transform=None):
        self.labels_df = labels_df
        self.url_map = url_map
        self.label_map = label_map
        self.transform = transform
        self.ids = list(url_map.keys())

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, idx):
        image_id = self.ids[idx]
        url = self.url_map[image_id]

        # Download image
        try:
            response = requests.get(url, timeout=10)
            img = Image.open(BytesIO(response.content)).convert("RGB")
        except:
            return self.__getitem__((idx + 1) % len(self.ids))

        width, height = img.size
        records = self.labels_df[self.labels_df["ImageID"] == image_id]
        boxes = []
        labels = []
        for _, row in records.iterrows():
            # Dummy boxes: you can replace this with real bounding boxes if available
            # For now, use full image as bbox
            boxes.append([0, 0, width, height])
            labels.append(self.label_map[row["LabelName"]])

        boxes = torch.tensor(boxes, dtype=torch.float32)
        labels = torch.tensor(labels, dtype=torch.int64)

        target = {"boxes": boxes, "labels": labels}
        if self.transform:
            img = self.transform(img)

        return img, target

# === INIT DATASET & MODEL ===
transform = ToTensor()
dataset = OpenImagesDataset(labels_csv, url_map, label_map, transform=transform)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True, collate_fn=lambda x: tuple(zip(*x)))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = fasterrcnn_resnet50_fpn(pretrained=True)
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, len(label_map) + 1)
model.to(device)

# === TRAIN ===
optimizer = torch.optim.SGD(model.parameters(), lr=0.005, momentum=0.9, weight_decay=0.0005)
model.train()

# Add a progress bar for training
for epoch in range(1):
    epoch_loss = 0
    for images, targets in tqdm(dataloader, desc=f"Epoch {epoch+1}", unit="batch"):
        images = [img.to(device) for img in images]
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
        loss_dict = model(images, targets)
        losses = sum(loss for loss in loss_dict.values())
        optimizer.zero_grad()
        losses.backward()
        optimizer.step()
        epoch_loss += losses.item()

    print(f"Epoch {epoch+1}: Loss = {epoch_loss:.4f}")

# === INFERENCE ===
model.eval()
img, _ = dataset[0]
with torch.no_grad():
    pred = model([img.to(device)])

# Add a progress bar for inference
img_np = img.permute(1, 2, 0).numpy()
plt.figure(figsize=(8, 8))
plt.imshow(img_np)
ax = plt.gca()

# Show bounding boxes
for box, label in zip(pred[0]['boxes'], pred[0]['labels']):
    x1, y1, x2, y2 = box.cpu()
    rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, edgecolor='red', facecolor='none')
    ax.add_patch(rect)
    ax.text(x1, y1 - 5, f"Class {label.item()}", color='yellow', backgroundcolor='black')

plt.axis("off")
plt.show()
