from typing import Optional


def score_result(title: str, product: str, product_code: Optional[str] = None) -> float:
    score = 0.0
    title_lower = title.lower()
    product_lower = product.lower()

    # award points for each product name word found in the title
    product_words = product_lower.split()
    matches = sum(1 for word in product_words if word in title_lower)
    score += matches / len(product_words)

    # keep score between 0.0 and 1.0
    return round(min(max(score, 0.0), 1.0), 2)


# TODO: add product code match bonus
#    if product_code and product_code.lower() in title_lower:
        score += 0.4
# TODO: add positive signals (official, press, spec)
#score += 0.1
# TODO: add negative signals (review, vs, alternative, clone)
#score -= 0.2
