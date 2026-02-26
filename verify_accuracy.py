import os
import pandas as pd
import time
import psutil
from app.services.engine_service import find_answer

def measure_ram():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

def run_benchmarks():
    print("--- Starting Optimization Benchmark ---")
    start_ram = measure_ram()
    print(f"Initial RAM Usage: {start_ram:.2f} MB")

    # Load a sample CSV
    test_csv = "data/chatbots/1/faqs.csv"
    if not os.path.exists(test_csv):
        # Create a mock CSV if it doesn't exist for testing
        os.makedirs("data/chatbots/1", exist_ok=True)
        df = pd.DataFrame({
            "Question": ["What is FAQSense?", "How do I install it?", "Is it free?"],
            "Answer": ["AI chatbot platform.", "Run npm install.", "Yes, it has a free tier."]
        })
        df.to_csv(test_csv, index=False)

    test_queries = [
        "What is this tool about?",
        "instruction for installation",
        "do i have to pay?",
        "completely unrelated gibberish"
    ]

    print(f"\nTesting {len(test_queries)} queries...")
    
    for query in test_queries:
        start_time = time.time()
        answer, matched_q = find_answer(1, test_csv, query)
        duration = (time.time() - start_time) * 1000
        print(f"\nQuery: '{query}'")
        print(f"Response: '{answer}' (Matched: '{matched_q}')")
        print(f"Latency: {duration:.2f} ms")

    final_ram = measure_ram()
    print(f"\nFinal RAM Usage: {final_ram:.2f} MB")
    print(f"RAM Increase during execution: {final_ram - start_ram:.2f} MB")
    print("--- Benchmark Complete ---")

if __name__ == "__main__":
    run_benchmarks()
