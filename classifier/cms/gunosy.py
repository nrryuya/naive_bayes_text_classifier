#諸々の機能を具体的にテストするためのプログラムである。

from scraper import get_title
# import sqlite3
# import os
# import lxml.html  # @UnresolvedImport
# import requests
import sys
import os

#本テストプログラムは、外部からモデル(Article)をいじろうとしている。この観点で調べなおすとよい。
# プロジェクトのパッケージを sys.path に追加する
sys.path.append('c:\\work\\gunosy\\classifier\\classifier\\')

# 環境変数 DJANGO_SETTINGS_MODULE にプロジェクトの settings をセット
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


from models import Article

target_url = 'https://gunosy.com/articles/a0NQi'
title = get_title(target_url)
category = 'カテゴリー1'

#データベースに追加されている気配がない
# os.chdir(os.pardir)#db.sqlite3があるのは一つ上の階層であり、そこに移動してからやらないと、cms下にデータベースが作られる。
# conn = sqlite3.connect('./db.sqlite3')
# cur = conn.cursor()
# cur.execute("""INSERT INTO cms_article (url, title ,category, id)values(?,?,?,NULL)""", (target_url, title, category)) #「"""」囲う範囲がポイント

p = Article.objects.create(title=title, url=target_url, category=category)


# #スクレイピングのテスト(done)
# target_html = requests.get('https://gunosy.com/categories/2?page=20').text
# root = lxml.html.fromstring(target_html)
# article_list = root.cssselect('.list_content .list_title a') #どうしてリストとして取得されるのだろうか。
# for a in article_list:
#     print(a.attrib['href'])
#             