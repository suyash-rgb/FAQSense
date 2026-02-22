from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

def test_logic():
    questions = ["What are your hours?", "Do you offer refunds?"]
    
    test_cases = [
        ("When is the shop open?", "What are your hours?"),
        ("What time do you close?", "What are your hours?"),
        ("Can I get my money back?", "Do you offer refunds?"),
        ("How do I return this?", "Do you offer refunds?"),
        ("tell me a joke", "NONE")
    ]
    
    faq_embeddings = model.encode(questions, convert_to_tensor=True)
    
    for query, expected in test_cases:
        query_embedding = model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, faq_embeddings)[0]
        best_score_idx = cos_scores.argmax().item()
        best_score = cos_scores[best_score_idx].item()
        
        print(f"Query: {query}")
        print(f"Best Match: {questions[best_score_idx]} (Score: {best_score:.4f})")
        print("-" * 20)

if __name__ == "__main__":
    test_logic()
