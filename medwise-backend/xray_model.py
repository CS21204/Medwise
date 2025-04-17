import torch
from torchvision import models, transforms
from PIL import Image
import io

model = models.resnet18(pretrained=True)
model.fc = torch.nn.Linear(model.fc.in_features, 2)  # e.g., Normal vs Pneumonia
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

async def predict_xray(file):
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(tensor)
    prediction = torch.softmax(output, dim=1)[0].tolist()
    return {"class": int(torch.argmax(output)), "confidence": prediction}
