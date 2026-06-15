# src/models/test_model.py

import joblib
import sys

print("Loading model...")
model = joblib.load("src/models/category_model.pkl")

# --- Test cases: input → expected category
test_cases = [
    ("SWIGGY ORDER",          "Food"),
    ("ZOMATO ORDER",          "Food"),
    ("UBER TRIP",             "Travel"),
    ("OLA CAB",               "Travel"),
    ("AMAZON PURCHASE",       "Shopping"),
    ("FLIPKART SALE",         "Shopping"),
    ("NETFLIX SUBSCRIPTION",  "Entertainment"),
    ("SPOTIFY PREMIUM",       "Entertainment"),
]

print("Running tests...\n")

passed = 0
failed = 0

for description, expected in test_cases:
    predicted = model.predict([description])[0]
    status = "✅ PASS" if predicted == expected else "❌ FAIL"
    if predicted == expected:
        passed += 1
    else:
        failed += 1
    print(f"  {status}  |  {description:<28} → {predicted} (expected: {expected})")

print(f"\nResults: {passed} passed, {failed} failed out of {len(test_cases)} tests")

if failed > 0:
    print("Tests FAILED — model is not predicting correctly")
    sys.exit(1)   # ← makes GitHub Actions mark the run as failed

print("All tests passed ✅")