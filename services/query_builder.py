from typing import Optional, List


def build_queries(product: str, product_code: Optional[str] = None) -> List[str]:
    # base queries for every product search
    queries = [
        f'"{product}" official image',
        f'"{product}" product photo',
        f'{product} press kit image',
    ]

    # product code queries narrow the results to the exact model
    if product_code:
        queries += [
            f'"{product_code}" {product}',
            f'"{product_code}" product image',
        ]

    return queries
