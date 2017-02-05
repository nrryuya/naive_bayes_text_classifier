import math
import sys
import os
import pickle
from scraper.scraper import get_title, extract_words


class Classifier():

    def __init__(self):
        self.categories = set(
            ['エンタメ', 'スポーツ', 'おもしろ', '国内',
             '海外', 'コラム', 'IT・科学', 'グルメ'])  # カテゴリの集合

    def score(self, words):  # 名詞群から事後確率の分子の対数を計算

        BASE = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(BASE, 'word_count.pickle'), mode='rb') as w:
            word_count = pickle.load(w)
        with open(os.path.join(BASE, 'cat_count.pickle'), mode='rb') as c:
            cat_count = pickle.load(c)
        with open(os.path.join(BASE, 'prior_probs.pickle'), mode='rb') as p:
            prior_probs = pickle.load(p)

        score = {}
        word_probs = {}
        for cat in self.categories:
            word_probs[cat] = {}
            score[cat] = 0  # 他にも書き方あると思われる
            score[cat] += math.log(prior_probs[cat])
            for word in words:
                if word in word_count[cat]:
                    word_probs[cat][word] = word_count[
                        cat][word] / cat_count[cat]
                else:
                    # ラプラススムージング
                    # pickleできる形式の制限からlambdaを使うdefaultdictは使えず
                    word_probs[cat][word] = 1 / cat_count[cat]
                    # 全部else側にきてない？
                score[cat] += math.log(word_probs[cat][word])
        return score

    def best_cat(self, score):  # scoreから、scoreが最大なcatを返す
        best_cat = None
        max_score = -sys.maxsize
        for cat in self.categories:
            if score[cat] > max_score:
                max_score = score[cat]
                best_cat = cat
        return best_cat

    def classify(self, url):
        words = extract_words(url)
        score = self.score(words)
        category = self.best_cat(score)  # カテゴリ判別完了

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
# with open('cat_count.pickle', mode='rb') as c:
#     cat_count = pickle.load(c)
# with open('prior_probs.pickle', mode='rb') as p:
#     prior_probs = pickle.load(p)
#
# # print(word_count)
# print(cat_count)
# print(prior_probs)
