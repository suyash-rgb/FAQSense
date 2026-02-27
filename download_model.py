import os
from fastembed import TextEmbedding

def download_model():
    model_name = "BAAI/bge-small-en-v1.5"
    print(f"Downloading/Caching FastEmbed model '{model_name}'...")
    # This will download and cache the model in the default fastembed location
    # On Render, it's better to let it cache during build so it's ready at runtime
    _ = TextEmbedding(model_name=model_name)
    print("Model initialized and cached successfully.")

if __name__ == "__main__":
    download_model()
