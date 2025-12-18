from app.services.keyword_scanner import scan_text, should_analyze_with_llm, ScanResult

def print_result(text, result: ScanResult):
    print(f"\nText: {text}")
    print(f"  Severity: {result.keyword_severity}")
    print(f"  Churn: {result.churn_signals}")
    print(f"  Positive: {result.positive_signals}")
    print(f"  Action: {result.action_signals}")
    print(f"  Compliance: {result.compliance_signals}")
    print(f"  Should Analyze: {should_analyze_with_llm(result)}")

# Test 1: Positive
text1 = "I love this product, it is amazing!"
result1 = scan_text(text1)
print_result(text1, result1)

# Test 2: Critical Churn
text2 = "We are evaluating alternatives and might terminate the contract."
result2 = scan_text(text2)
print_result(text2, result2)

# Test 3: Compliance (FedRAMP)
text3 = "Does this support FedRAMP or HIPAA?"
result3 = scan_text(text3)
print_result(text3, result3)

# Test 4: Action Signals
text4 = "I'll send the document by Friday. Can you send the pricing?"
result4 = scan_text(text4)
print_result(text4, result4)

# Test 5: Mixed / Low signal
text5 = "Just checking in on the ticket."
result5 = scan_text(text5)
print_result(text5, result5)
