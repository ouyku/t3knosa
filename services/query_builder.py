from typing import Optional, List


def build_queries(
    product: str,
    product_code: Optional[str] = None,
    brand_site: Optional[str] = None
) -> List[str]:
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

    # brand site query — tells google to search only on that domain
    if brand_site:
        queries.append(f'site:{brand_site} "{product}"')

    return queries
