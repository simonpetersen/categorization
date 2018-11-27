from mrjob.job import MRJob
from mrjob.step import MRStep
from utils.DbConnection import DbConnection


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
        categories = sorted_counts[:10]
        return categories

    def steps(self):
        return [MRStep(mapper=self.mapper, combiner=self.combiner_count_words,
                       reducer=self.reducer_count_words),
                MRStep(reducer=self.reducer_find_max)]


if __name__ == '__main__':
    MRCategorizer.run()
