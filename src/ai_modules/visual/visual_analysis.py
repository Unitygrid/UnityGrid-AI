import torch
from torchvision import models, transforms
from PIL import Image
import io

# Load a pre-trained ResNet model
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
model.eval()

# Define the image transformations
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Define a function to analyze the image
def analyze_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = preprocess(image)
    image = image.unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        outputs = model(image)
    _, predicted = torch.max(outputs, 1)
    
    return predicted.item()