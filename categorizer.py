from mrjob.job import MRJob
from mrjob.step import MRStep
from utils.db import DbConnection
import os

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


class MRCategorizerAll(MRJob):

    db = DbConnection("utils/WikiDB.sqlite")
    ignored_words = db.getIgnoreList()

    def mapper(self, _, line):
        filename = os.environ["map_input_file"]
        for word in line.split():
            yield filename + ':' + word.lower(), 1

    def combiner_count_words(self, key, values):
        yield key, sum(values)

    def reducer_remove_stopwords(self, key, values):
        keyword = key.split(':')[1]
        if keyword not in MRCategorizer.ignored_words:
            yield None, (key, sum(values))

    def reducer_find_categories(self, _, word_counts):
        sorted_counts = sorted(list(word_counts), key=lambda w: w[1], reverse=True)
        count_threshold = 20
        sorted_counts2 = list(filter(lambda c: c[1] >= count_treshold, sorted_counts))
        categories = []
        merged_categories = []
        for count in sorted_counts2:
            word = count[0].split(':')[-1]
            matches_shorter = list(filter(lambda c: c[0].split(':')[-1][:len(word)] == word, categories))
            matches_longer = list(filter(lambda c: c[0].split(':')[-1] == word[:len(c[0].split(':')[-1])], categories))
            if len(matches_shorter) > 0 or len(matches_longer) > 0:
                merged_matches = matches_longer + matches_shorter
                # Finds the files associated with this category
                files_in_matches = merged_matches[0][0].split(':')[:-1]
                insert = False
                for i in files_in_matches:
                    if count[0].split(':')[0] == i:
                        insert = False
                        break
                    insert = True
                #Insert the new count into categories with the new filename appended to it
                if (insert):
                    count[0] = count[0].split(':')[0] + (':' + merged_matches[0][0])
                    #Removes old entry of category
                    index = categories.index(merged_matches[0])
                    del categories[index]
                else:
                    continue
            categories.append(count)
            if(len(count[0].split(':')[:-1]) > 1):
                for category in merged_categories:
                    if(category[0].split(':')[-1] == count[0].split(':')[-1]):
                        index = merged_categories.index(category)
                        del merged_categories[index]
                merged_categories.append(count)
            if len(merged_categories) == 10:
                return merged_categories
        return merged_categories + categories[:10 - len(merged_categories)]

    def steps(self):
        return [MRStep(mapper=self.mapper, combiner=self.combiner_count_words,
                       reducer=self.reducer_remove_stopwords),
                MRStep(reducer=self.reducer_find_categories)]



if __name__ == '__main__':
    MRCategorizer.run()
