from app.services.keyword_scanner import scan_text, should_analyze_with_llm

text1 = "I love this product!"
matches1 = scan_text(text1)
print(f"Text: {text1}")
print(f"Matches: {matches1}")
print(f"Should Analyze: {should_analyze_with_llm(matches1)}")

text2 = "I want to cancel my subscription appropriately."
matches2 = scan_text(text2)
print(f"\nText: {text2}")
print(f"Matches: {matches2}")
print(f"Should Analyze: {should_analyze_with_llm(matches2)}")

text3 = "We are switching to a competitor because it is too expensive."
matches3 = scan_text(text3)
print(f"\nText: {text3}")
print(f"Matches: {matches3}")
print(f"Should Analyze: {should_analyze_with_llm(matches3)}")
