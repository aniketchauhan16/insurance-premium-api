import pickle
import pandas as pd

# ml_flow
MODEL_VERSION = '1.0.0'

# importing ml model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Ensure class labels are standard Python strings/ints, not numpy types
class_labels = [str(label) for label in model.classes_.tolist()]

def predict_output(user_input: dict):

    df = pd.DataFrame([user_input])

    # 1. Cast predicted class explicitly to a native Python type (e.g., str or int)
    predicted_class = model.predict(df)[0]
    if hasattr(predicted_class, "item"): 
        predicted_class = predicted_class.item()

    # Get probabilities for all classes
    probabilities = model.predict_proba(df)[0]
    
    # 2. Convert confidence from np.float64 to native Python float
    confidence = float(max(probabilities))

    # 3. Zip and ensure the map converts each probability value to a standard float
    class_probs = dict(zip(class_labels, map(lambda p: round(float(p), 4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }