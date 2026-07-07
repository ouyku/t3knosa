from typing import Optional # bc product code might not exist


# scoring if the product is correctly identified or not
def score_result(title: str, product: str, product_code: Optional[str] = None) -> float:
    score = 0
    title_lower = title.lower()
    product_lower = product.lower()

    # award points for each product name word found in the title
    # like 2/3 words match so 0.66
    product_words = product_lower.split()
    matches = sum(1 for word in product_words if word in title_lower)
    score += matches / len(product_words)

    # product code is a strong signal — very specific so +0.4
    if product_code and product_code.lower() in title_lower:
        score += 0.4

    # add positive signs
    positive = ["official", "press", "product photo", "spec", "authentic"]
    for word in positive:
        if word in title_lower:
            score += 0.1

    # add very negative signs
    negative = ["unofficial", "replica", "imitation", "vs", "alternative", "teardown", "clone", "fake", "knockoff", "leak"]
    for word in negative:
        if word in title_lower:
            score -= 0.2

    # add not the most ideal signs
    notgood = ["unboxing", "review", "hands-on"]
    for word in notgood:
        if word in title_lower:
            score -= 0.1

    # penalize if numbers in query don't appear in title
    # model numbers are critical — "2220" and "2101" are completely different products
    import re
    query_numbers = re.findall(r'\d+', product_lower)
    for num in query_numbers:
        if num not in title_lower:
            score -= 0.5  # strong penalty for wrong model number

    # keep score between 0 and 1
    return round(min(max(score, 0), 1), 2)

