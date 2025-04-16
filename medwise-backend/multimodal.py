from chat import chat_with_bot
from xray_model import predict_xray

async def predict_multimodal(symptom_text, file):
    text_response = chat_with_bot(symptom_text)
    image_prediction = await predict_xray(file)
    risk_score = (image_prediction['confidence'][1]) * 100
    return {
        "chat_response": text_response,
        "xray_prediction": image_prediction,
        "risk_score_percent": round(risk_score, 2)
    }
