from rapidfuzz import fuzz

q = "I like turtles"
match = "How can I contact support?"

print(f"WRatio: {fuzz.WRatio(q, match)}")
print(f"Token Sort Ratio: {fuzz.token_sort_ratio(q, match)}")
print(f"Partial Ratio: {fuzz.partial_ratio(q, match)}")
print(f"Simple Ratio: {fuzz.ratio(q, match)}")
