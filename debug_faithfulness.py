from sentence_transformers import SentenceTransformer, util
import torch
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
    "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

def get_keywords(text: str) -> set:
    words = re.findall(r'\b\w+\b', text.lower())
    return {w for w in words if w not in STOP_WORDS}

def debug_faithfulness():
    questions = [
        "What are your hours?",
        "Do you offer refunds?",
        "How can I contact support?",
        "How can I contact sales?"
    ]
    
    test_queries = [
        "When is the shop open?",
        "How to contact them?",
        "When can I move in?"
    ]
    
    faq_embeddings = model.encode(questions, convert_to_tensor=True)
    
    with open("debug_results.txt", "w") as f:
        for query in test_queries:
            f.write(f"\nQUERY: {query}\n")
            query_embedding = model.encode(query, convert_to_tensor=True)
            cos_scores = util.cos_sim(query_embedding, faq_embeddings)[0]
            
            top_results = torch.topk(cos_scores, k=min(2, len(questions)))
            best_score = top_results.values[0].item()
            best_index = top_results.indices[0].item()
            second_best_score = top_results.values[1].item()
            
            matched_q = questions[best_index]
            f.write(f"  Best Match: '{matched_q}' (Score: {best_score:.4f})\n")
            f.write(f"  Second Best: '{questions[top_results.indices[1].item()]}' (Score: {second_best_score:.4f})\n")
            f.write(f"  Gap: {best_score - second_best_score:.4f}\n")
            
            query_kw = get_keywords(query)
            match_kw = get_keywords(matched_q)
            overlap = query_kw.intersection(match_kw)
            f.write(f"  Keywords Query: {query_kw}\n")
            f.write(f"  Keywords Match: {match_kw}\n")
            f.write(f"  Overlap: {overlap} (Count: {len(overlap)})\n")

if __name__ == "__main__":
    debug_faithfulness()
