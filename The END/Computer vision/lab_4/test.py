import torch
from PIL import Image
import torchvision.transforms.functional as F
from matplotlib import pyplot as plt
import matplotlib.patches as patches


def load_image_tensor(image_path, device):
    image = Image.open(image_path).convert('RGB')
    image_tensor = F.to_tensor(image).unsqueeze(0).to(device)
    return image_tensor

def predict_image(model, image_tensor):
    model.eval()
    with torch.no_grad():
        prediction = model(image_tensor)
    return prediction

def visualize_output(image_path, predictions, confidence_threshold=0.5):
    image = Image.open(image_path)
    plt.figure(figsize=(12, 8))
    plt.imshow(image)
    ax = plt.gca()

    if predictions and 'boxes' in predictions:
        boxes = predictions['boxes'].detach().cpu().numpy()
        labels = predictions['labels'].detach().cpu().numpy()
        scores = predictions['scores'].detach().cpu().numpy()

        for box, label, score in zip(boxes, labels, scores):
            if score > confidence_threshold:
                x1, y1, x2, y2 = box
                rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
                plt.text(x1, y1, f'{label}: {score:.2f}', bbox=dict(facecolor = 'yellow', alpha = 0.5))
    plt.axis('off')
    plt.show()


device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

image_paths = ['']

for image_path in image_paths:
    image_tensor = load_image_tensor(image_path, device)
    predictions = predict_image(model, image_tensor)
    visualize_output(image_path, predictions[0], confidence_threshold=0.5)
