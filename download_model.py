import os
from sentence_transformers import SentenceTransformer

def download_model():
    model_name = 'all-MiniLM-L6-v2'
    project_root = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_root, 'models', model_name)
    
    if not os.path.exists(model_path):
        print(f"Downloading model '{model_name}' to {model_path}...")
        model = SentenceTransformer(model_name)
        model.save(model_path)
        print("Model saved successfully.")
    else:
        print(f"Model already exists at {model_path}")

if __name__ == "__main__":
    download_model()
