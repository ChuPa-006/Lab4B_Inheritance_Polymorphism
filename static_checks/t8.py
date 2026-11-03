"""Original Task 8 snippet. Run pyflakes on this file to see the duplicate name."""


class ProductSearch:
    def __init__(self, products):
        self.products = products

    def search(self, query):
        q = query.lower()
        return [p for p in self.products if q in p["title"].lower()]

    def search(self, query, filters):
        q = query.lower()
        result = [p for p in self.products if q in p["title"].lower()]
        for key, value in filters.items():
            result = [p for p in result if p.get(key) == value]
        return result
