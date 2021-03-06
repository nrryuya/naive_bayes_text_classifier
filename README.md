# アプリの使い方

**記事の一覧**

* データベースに保存されている記事データのタイトル、URL、カテゴリを確認できます。

**記事の追加**

* URLを入力することで、テキスト分類器により記事のカテゴリを判定し、データベースにデータを保存します。

**記事の修正**

* データベースに保存されている記事データを変更できます。

# 実装について

**テキスト分類器の学習**
* /classifier/cms/training.pyをコマンドプロンプト上で実行することで学習されるようにしました。
* 8つのカテゴリそれぞれ、記事がリストになっているページ(例： https://gunosy.com/categories/1) の6ページから19ページまでを訓練データとしました。  
※1ページから5ページまでは分類器の評価用に使用しています。
* 学習により計算された各カテゴリの事前確率、単語の出現回数等はpickleによりシリアライズすることで保存しています。

**naive bayesによるテキスト分類器部分について**

* 記事URLから本文をスクレイピングし、形態素解析により名詞のみを取り出し、カテゴリ毎の事後確率を計算しています。
* 学習結果はpickleでデシリアライズして取り出しています。
* 事後確率の計算では、アンダーフロー防止のため対数をとっています。
* ラプラススムージングを採用しています。

**分類器の評価**

* /classifier/cms/evaluation.pyをコマンドプロンプト上で実行することでカテゴリ別及び全体の精度(正しいカテゴリの判別率)が計算されるようにしました。

* 精度は下記の通りです。

| カテゴリ | 精度 |
|:------:|:----:|
|合計|0.7725|
|グルメ|0.97|
|IT・科学|0.96|
|スポーツ|0.93|
|国内|0.67|
|コラム|0.83|
|エンタメ|0.75|
|海外|0.83|
|おもしろ|0.24|
