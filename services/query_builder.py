from typing import Optional, List


def build_queries(
    product: str,
    product_code: Optional[str] = None,
    brand_site: Optional[str] = None
) -> List[str]:
    if product_code:
        # lead with model code — most specific identifier, avoids brand name ambiguity
        queries = [
            f'"{product_code}" {product} product photo',
            f'"{product_code}" {product} official image',
            f'"{product_code}" product image electronics',
        ]
    else:
        # no model code — add "product" context to reduce ambiguity
        queries = [
            f'"{product}" product photo',
            f'"{product}" official product image',
            f'"{product}" electronics product',
        ]

    # brand site query — tells google to search only on that domain
    if brand_site:
        queries.append(f'site:{brand_site} "{product}" {product_code or ""}')

    return queries
