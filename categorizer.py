from mrjob.job import MRJob
from mrjob.step import MRStep
from utils.db import DbConnection


class MRCategorizer(MRJob):

    db = DbConnection("utils/WikiDB.sqlite")
    ignored_words = db.getIgnoreList()

    def mapper(self, _, line):
        for word in line.split():
            yield word.lower(), 1

    def combiner_count_words(self, key, values):
        yield key, sum(values)

    def reducer_count_words(self, key, values):
        if key not in MRCategorizer.ignored_words and key != 's':
            yield None, (sum(values), key)

    def reducer_find_max(self, _, word_counts):
        sorted_counts = sorted(list(word_counts), key=lambda w: w[0], reverse=True)
        categories = []
        for count in sorted_counts:
            word = count[1]
            matches = list(filter(lambda c: c[1] == word[:len(c[1])], categories))
            if len(matches) > 0:
                continue
            categories.append(count)
            if len(categories) == 10:
                return categories
        return categories

    def steps(self):
        return [MRStep(mapper=self.mapper, combiner=self.combiner_count_words,
                       reducer=self.reducer_count_words),
                MRStep(reducer=self.reducer_find_max)]


if __name__ == '__main__':
    MRCategorizer.run()
