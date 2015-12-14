# -*- coding: utf-8 -*-

import copy, random

class GeneticAlgorithm:
    def __init__(self, goods, res):
        self.goods = goods
        self.res = res
        self._rescount = [rs["qnt"] for rs in self.res]
        self._goodcost = [good["cost"] for good in self.goods]
        self._goodprice = [good["price"] for good in self.goods]
        self._popsize = 100
        self._chosen = 10
        self._mut = 20
        self._break = 5

    def solve(self):
        br = 0
        maxfit = 0
        bestsln = {"fitness": 0, "chrom": [0] * len(self.goods)}
        chroms = self._randomChromosomes(self._popsize)
        pop = [{"chrom": chrom, "fitness": self._fitness(chrom)}
            for chrom in chroms]
        while br < self._break:
            chosen = self._weightedChoice(pop, self._chosen)
            newpop = list(chosen)
            while len(newpop) < self._popsize:
                s1, s2 = self._weightedChoice(chosen, 2)
                cr = self._crossingover(s1["chrom"], s2["chrom"])
                newpop.append({"fitness": self._fitness(cr), "chrom": cr})
            children = [sln for sln in newpop if sln not in chosen]
            if children:
                for _ in range(self._mut):
                    child = random.choice(children)
                    self._mutateInplace(child)
            pop_bestsln = max(newpop, key = lambda x: x["fitness"])
            pop_maxfit = self._fitness(pop_bestsln["chrom"])
            if maxfit < pop_maxfit:
                maxfit = pop_maxfit
                bestsln = pop_bestsln
            else:
                br += 1
            pop = newpop
        return {"profit": bestsln["fitness"],
                "items": [{"name": self.goods[ind]["name"],
                    "count": qnt} for ind, qnt in enumerate(bestsln["chrom"])]}

    def _fitness(self, chrom):
        res = list(self._rescount)
        for gdind, count in enumerate(chrom):
            for resind, cost in enumerate(self._goodcost[gdind]):
                res[resind] -= cost*count
                if res[resind] < 0:
                    return 0
        return sum(self._goodprice[gdind]*count
            for gdind, count in enumerate(chrom))

    def _randomChromosomes(self, count):
        chromosomes = []
        curgood = 0
        for _ in range(count):
            res = list(self._rescount)
            goodcount = 0
            while not any(rs < 0 for rs in res):
                goodcount += 1
                for resind, cost in enumerate(self._goodcost[curgood]):
                    res[resind] -= cost
            count = random.randrange(goodcount)
            chromosomes.append([0]*curgood + [count] + [0]*(len(self.goods)-curgood-1))
            curgood = (curgood + 1) % len(self.goods)
        return chromosomes

    def _weightedChoice(self, pop, count):
        pop = list(pop)
        chosen = []
        for _ in range(count):
            total = sum(sln["fitness"] for sln in pop)
            if total == 0:
                ind = random.randrange(len(pop))
            else:
                ch = random.randrange(total)
                acc = 0
                ind = 0
                while acc <= ch:
                    acc += pop[ind]["fitness"]
                    ind += 1
                ind -= 1
            chosen.append(pop[ind])
            del pop[ind]
        return chosen

    def _crossingover(self, ch1, ch2):
        i = random.randrange(len(self.goods))
        return ch1[:i] + ch2[i:]

    def _mutateInplace(self, chrom):
        for _ in range(random.randrange(len(chrom)//2)):
            i = random.randrange(len(chrom))
            chrom[i] = int(chrom[i] * (random.random() + 0.5))