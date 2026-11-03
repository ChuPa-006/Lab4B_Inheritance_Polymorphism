"""Task 8 - One search method with optional filters."""



from collections.abc import Mapping


class ProductSearch:
    def __init__(self, products: list[dict[str, object]]) -> None:
        self.products = products

    def search(
        self,
        query: str,
        *,
        filters: Mapping[str, object] | None = None,
    ) -> list[dict[str, object]]:
        q = query.lower()
        result = [
            product
            for product in self.products
            if q in str(product.get("title", "")).lower()
        ]
        if filters is not None:
            for key, value in filters.items():
                result = [product for product in result if product.get(key) == value]
        return result


def test_search_without_filters():
    search = ProductSearch([{"title": "iPhone 15", "brand": "Apple"}])
    assert search.search("iphone") == [{"title": "iPhone 15", "brand": "Apple"}]


def test_search_with_keyword_only_filter_dictionary():
    products = [
        {"title": "iPhone 15", "brand": "Apple"},
        {"title": "Galaxy S24", "brand": "Samsung"},
        {"title": "iPhone 14", "brand": "Apple"},
    ]
    search = ProductSearch(products)
    assert search.search("iphone", filters={"brand": "Apple"}) == [
        {"title": "iPhone 15", "brand": "Apple"},
        {"title": "iPhone 14", "brand": "Apple"},
    ]


def test_empty_filter_dictionary_behaves_like_no_filters():
    search = ProductSearch([{"title": "iPhone 15", "brand": "Apple"}])
    assert search.search("iphone", filters={}) == search.search("iphone")
