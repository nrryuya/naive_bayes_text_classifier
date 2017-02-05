import lxml.html  # @UnresolvedImport
import requests
from scraper.scraper import extract_words
import pickle
import sys
import os
from django.conf import settings
sys.path.append(os.pardir)


class Training:  # クラスにする意味があるのだろうか？

    def __init__(self):
        self.categories = set(
            ['エンタメ', 'スポーツ', 'おもしろ', '国内',
             '海外', 'コラム', 'IT・科学', 'グルメ'])  # カテゴリの集合
        self.categorycount = {}      # categorycount[category] カテゴリの出現回数
        self.wordcount = {}     # wordcount[category][word] カテゴリでの単語の出現回数

        for category in self.categories:
            self.categorycount[category] = 0
            self.wordcount[category] = {}

    # https://gunosy.com/の8つのカテゴリの6～20ページを教師データとして取得
    def make_trainig_data(self):
        serial_category = {1: 'エンタメ', 2: 'スポーツ', 3: 'おもしろ',
                           4: '国内', 5: '海外', 6: 'コラム', 7: 'IT・科学', 8: 'グルメ'}
        training_data = []  # リスト型として作成
        for i in range(1, 9):
            category = serial_category[i]  # 記事のカテゴリー
            for j in range(6, 20):
                target_html = requests.get(
                    'https://gunosy.com/categories/' +
                    str(i) + '?page=' + str(j)).text
                root = lxml.html.fromstring(target_html)
                article_list = root.cssselect(
                    '.list_content .list_title a')  # どうしてリストとして取得されるのだろうか。
                for a in article_list:
                    url = a.attrib['href']  # 記事のurl
                    title = a.text_content  # 記事のタイトル
                    training_data.append(
                        {'url': url, 'title': title, 'category': category})
        return training_data

    # training_data(カテゴリ、urlが辞書になったデータのリスト)からカテゴリーの頻度、カテゴリー別の単語の頻度を算出
    def count(self, training_data):
        for d in training_data:
            category = d['category']
            words = extract_words(d['url'])  # training_dataは要素が辞書型なリスト型を想定
            self.categorycount[category] += 1
            for word in words:
                if word in self.wordcount[category]:  # そのカテゴリーでその単語は既に出ているか？
                    self.wordcount[category][word] += 1
                else:
                    self.wordcount[category][word] = 1

    def prior_prob(self, category):  # カテゴリの事前確率
        num_of_training_data = 0
        for category in self.categories:
            num_of_training_data += self.categorycount[category]
        return self.categorycount[category] / num_of_training_data

    def train(self):  # 各カテゴリの事前確率と、カテゴリ別の単語の登場頻度の辞書データをシリアライズ
        training_data = self.make_trainig_data()
        self.count(training_data)
        prior_probs = {}  # 各カテゴリの事前確率
        for category in self.categories:
            prior_probs[category] = self.prior_prob(category)

        return self.wordcount, self.categorycount, prior_probs


t = Training()
wordcount, categorycount, priorprobs = t.train()

# BASE = os.path.dirname(os.path.abspath(__file__))
#
# with open(os.path.join(BASE, 'word_count.pickle'), mode='wb') as w:
#     pickle.dump(wordcount, w)
# with open(os.path.join(BASE, 'cat_count.pickle'), mode='wb') as c:
#     pickle.dump(catcount, c)
# with open(os.path.join(BASE, 'prior_probs.pickle'), mode='wb') as p:
#     pickle.dump(priorprobs, p)

with open(os.path.join(settings.PICKLE_PATH, 'word_count.pickle'), mode='wb') as w:
    pickle.dump(wordcount, w)
with open(os.path.join(settings.PICKLE_PATH, 'cat_count.pickle'), mode='wb') as c:
    pickle.dump(categorycount, c)
with open(os.path.join(settings.PICKLE_PATH, 'prior_probs.pickle'), mode='wb') as p:
    pickle.dump(priorprobs, p)


print('Training done')
