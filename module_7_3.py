class WordsFinder:
    def __init__(self, *file_names):
        self.file_names = file_names

    def get_all_words(self):
        all_words = {}
        punctuation = [',', '.', '=', '!', '?', ';', ':', ' - ']

        for file_name in self.file_names:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    cont = file.read().lower()
            except FileNotFoundError:
                with open(file_name, 'w', encoding='utf-8'):
                    cont = ''

            for i in punctuation:
                cont = cont.replace(i, '')

            words = cont.split()
            all_words[file_name] = words

        return all_words

    def find(self, word):
        word = word.lower()
        positions = {}

        for file_name, words in self.get_all_words().items():
            if word in words:
                positions[file_name] = words.index(word) + 1
            else:
                positions[file_name] = -1
        return positions

    def count(self, word):
        word = word.lower()
        counts = {}

        for file_name, words in self.get_all_words().items():
            counts[file_name] = words.count(word)
        return counts


finder1 = WordsFinder('Mother Goose - Monday’s Child.txt',)
print(finder1.get_all_words())
print(finder1.find('Child'))
print(finder1.count('Child'))

finder2 = WordsFinder('test_file.txt')
print(finder2.get_all_words()) # Все слова
print(finder2.find('TEXT')) # 3 слово по счёту
print(finder2.count('teXT')) # 4 слова teXT в тексте всего
