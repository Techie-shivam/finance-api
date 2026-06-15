import joblib

model = joblib.load(
    "src/models/category_model.pkl"
)

def predict_category(text):

    return model.predict([text])[0]