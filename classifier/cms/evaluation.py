from classifier.classifier import Classifier
import lxml.html  # @UnresolvedImport
import requests
import sys
import os
sys.path.append(os.pardir)


class Evaluation():

    def __init__(self):
        self.categories = set(
            ['エンタメ', 'スポーツ', 'おもしろ', '国内',
             '海外', 'コラム', 'IT・科学', 'グルメ'])  # カテゴリの集合

    def make_test_data(self):  # https://gunosy.com/の8つのカテゴリの6～20ページを教師データとして取得
        serial_category = {1: 'エンタメ', 2: 'スポーツ', 3: 'おもしろ',
                           4: '国内', 5: '海外', 6: 'コラム', 7: 'IT・科学', 8: 'グルメ'}
        test_data = []  # リスト型として作成
        for i in range(1, 9):
            category = serial_category[i]  # 記事のカテゴリー
            for j in range(1, 6):
                target_html = requests.get(
                    'https://gunosy.com/categories/' +
                    str(i) + '?page=' + str(j)).text
                root = lxml.html.fromstring(target_html)
                article_list = root.cssselect(
                    '.list_content .list_title a')  # どうしてリストとして取得されるのだろうか。
                for a in article_list:
                    url = a.attrib['href']  # 記事のurl
                    title = a.text_content  # 記事のタイトル
                    test_data.append(
                        {'url': url, 'title': title, 'category': category})
        return test_data

    def make_check_data(self, test_data):
        check_data = []  # 要素が辞書型のリスト型
        for d in test_data:
            title, url, classified_category = Classifier().classify(d['url'])
            ans_category = d['category']
            if classified_category == ans_category:
                true_false = 1
            else:
                true_false = 0
            check_data.append({'url': url, 'title': title,
                               'classified_category': classified_category,
                               'ans_category': ans_category,
                               'true_false': true_false})
        return check_data

    def evaluate(self):
        check_data = self.make_check_data(self.make_test_data())

        num_of_true = {}  # カテゴリ毎に正答数はいくつか
        category_count = {}  # カテゴリ毎にテスト用データはいくつあるか
        # 初期化
        for category in self.categories:
            num_of_true[category] = 0
            category_count[category] = 0

        for d in check_data:
            category_count[d['ans_category']] += 1
            if d['true_false'] == 1:
                num_of_true[d['ans_category']] += 1

        accuracy = {}
        total_of_true = 0  # カテゴリ無関係の正答数
        total_of_article = 0  # test_dataの記事数

        for category in self.categories:
            accuracy[category] = num_of_true[category] / category_count[category]
            total_of_true += num_of_true[category]
            total_of_article += category_count[category]

        total_accuracy = total_of_true / total_of_article

        accuracy.update({'合計': total_accuracy})

        return accuracy


e = Evaluation()
print(e.evaluate())
print('Evaluation done')
