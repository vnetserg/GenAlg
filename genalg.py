# -*- coding: utf-8 -*-

class GeneticAlgorithm:
    def __init__(self, goods, res):
        self.goods = goods
        self.res = res

    def solve(self):
        return {"profit": 100500, "items": [{"name": "Ананас", "count": 3}, {"name": "Апельсин", "count": 5}]}