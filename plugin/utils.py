# myapp/utils.py
import json
from PIL import Image
from torchvision import transforms
import torch
import torchvision.models as models
from PIL import Image


def extract_body_measurements(image_path):
    # Load and preprocess the image
    image = Image.open(image_path)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
                             0.229, 0.224, 0.225]),
    ])
    image = preprocess(image).unsqueeze(0)
    resnet = models.resnet18(pretrained=True)
    # Use the pre-trained ResNet model to extract the body measurements
    resnet.eval()
    with torch.no_grad():
        body_measurements = resnet(image)
    body_measurements = body_measurements.tolist()
    return json.dumps(body_measurements)


def compare_measurements(body_measurements, clothing_measurements):
    recommendations = []
    for clothing in clothing_measurements:
        # Compare the body measurements with the clothing measurements
        # and calculate a score
        score = calculate_score(body_measurements, clothing.measurements)
        if score > 0.8:
            recommendations.append(clothing)
    return recommendations


def calculate_score(body_measurements, clothing_measurements):
    # Compare the body measurements with the clothing measurements
    # and calculate a score
    score = 0
    for measurement in body_measurements:
        if measurement in clothing_measurements:
            score += 1
    return score/len(body_measurements)
