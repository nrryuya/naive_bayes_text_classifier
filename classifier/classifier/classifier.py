import math
import sys
import os
import pickle
from collections import defaultdict
from django.conf import settings
from scraper.scraper import get_title, extract_words
from classifier.consts import CATEGORY_SET


class Classifier():

    def __init__(self):
        self.categories = CATEGORY_SET
    def category_scores(self, words):  # 名詞群から事後確率の分子の対数を計算

        # BASE = os.path.dirname(os.path.abspath(__file__))
        # with open(os.path.join(BASE, 'word_count.pickle'), mode='rb') as w:
        #     word_count = pickle.load(w)
        # with open(os.path.join(BASE, 'cat_count.pickle'), mode='rb') as c:
        #     cat_count = pickle.load(c)
        # with open(os.path.join(BASE, 'prior_probs.pickle'), mode='rb') as p:
        #     prior_probs = pickle.load(p)

        with open(os.path.join(settings.PICKLE_PATH, 'word_count.pickle'), mode='rb') as w:
            word_count = pickle.load(w)
        with open(os.path.join(settings.PICKLE_PATH, 'category_count.pickle'), mode='rb') as c:
            category_count = pickle.load(c)
        with open(os.path.join(settings.PICKLE_PATH, 'prior_probs.pickle'), mode='rb') as p:
            prior_probs = pickle.load(p)

        category_scores = defaultdict(int)
        word_probs = {}
        for category in self.categories:
            word_probs[category] = {}
            category_scores[category] += math.log(prior_probs[category])
            for word in words:
                if word in word_count[category]:
                    word_probs[category][word] = word_count[
                        category][word] / category_count[category]
                else:
                    # ラプラススムージング
                    word_probs[category][word] = 1 / category_count[category]
                category_scores[category] += math.log(word_probs[category][word])
        return category_scores

    def best_category(self, category_scores):  # scoreから、scoreが最大なcategoryを返す
        best_category = None
        max_score = -sys.maxsize
        for category in self.categories:
            if category_scores[category] > max_score:
                max_score = category_scores[category]
                best_category = category
        return best_category

    def classify(self, url):
        words = extract_words(url)
        category_scores = self.category_scores(words)
        category = self.best_category(category_scores)  # カテゴリ判別完了

        title = get_title(url)
        return title, url, category

    def save_article(self, title, url, category):  # url,タイトル、カテゴリをデータベースに保存する。
        # classifier.pyからimportするevaluationをコマンドプロンプトから起動する関係で、この位置にしてある
        from cms.models import Article
        Article.objects.create(
            title=title, url=url, category=category)  # データベースに保存

# c=classifier()
# print(c.score(['ドジャース','鍋','可能']))

# with open('word_count.pickle', mode='rb') as w:
#     word_count = pickle.load(w)
# with open('category_count.pickle', mode='rb') as c:
#     category_count = pickle.load(c)
# with open('prior_probs.pickle', mode='rb') as p:
#     prior_probs = pickle.load(p)
#
# # print(word_count)
# print(category_count)
# print(prior_probs)
