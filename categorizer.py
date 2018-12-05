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

    def reducer_remove_stopwords(self, key, values):
        if key not in MRCategorizer.ignored_words:
            yield None, (key, sum(values))

    def reducer_find_categories(self, _, word_counts):
        sorted_counts = sorted(list(word_counts), key=lambda w: w[1], reverse=True)
        categories = []
        for count in sorted_counts:
            word = count[0]
            matches_shorter = list(filter(lambda c: c[0][:len(word)] == word, categories))
            matches_longer = list(filter(lambda c: c[0][:len(word)] == word[:len(c[0])], categories))
            if len(matches_shorter) > 0 or len(matches_longer) > 0:
                continue
            categories.append(count)
            if len(categories) == 10:
                return categories
        return categories

    def steps(self):
        return [MRStep(mapper=self.mapper, combiner=self.combiner_count_words,
                       reducer=self.reducer_remove_stopwords),
                MRStep(reducer=self.reducer_find_categories)]


if __name__ == '__main__':
    MRCategorizer.run()
