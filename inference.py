import joblib
import pandas as pd
from utils import preprocess_message

# Modelni yuklash
MODEL_PATH = "models/ddos_rf_model.pkl"
rf_model = joblib.load(MODEL_PATH)

def predict_ddos(message):
    """
    Xabarni bashorat qilish: DDoS yoki xavfsiz.
    """
    data = preprocess_message(message)  # Ma'lumotni qayta ishlash
    df = pd.DataFrame([data])  # Xabarni DataFrame ko‘rinishiga o‘tkazish
    prediction = rf_model.predict(df)  # Model yordamida bashorat qilish
    return prediction[0]  # Natijani qaytarish


