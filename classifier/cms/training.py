import lxml.html  # @UnresolvedImport
import requests
import pickle
import sys,os
sys.path.append(os.pardir)
from cms.scraper import extract_words



class Training:#クラスにする意味があるのだろうか？
    def __init__(self):
        self.categories = set(['エンタメ','スポーツ','おもしろ','国内','海外','コラム','IT・科学','グルメ']) # カテゴリの集合
        self.catcount = {}      # catcount[cat] カテゴリの出現回数
        self.wordcount = {}     # wordcount[cat][word] カテゴリでの単語の出現回数
        
        for cat in self.categories:
            self.catcount[cat] = 0
            self.wordcount[cat] = {}
        

    def make_trainig_data(self): #https://gunosy.com/の8つのカテゴリの6～20ページを教師データとして取得
        serial_cat = {1:'エンタメ',2:'スポーツ',3:'おもしろ',4:'国内',5:'海外',6:'コラム',7:'IT・科学',8:'グルメ'}
        training_data = []#リスト型として作成
        for i in range(1,9):
            category = serial_cat[i] #記事のカテゴリー
            for j in range(6,20):
                target_html = requests.get('https://gunosy.com/categories/'+str(i)+'?page='+str(j)).text
                root = lxml.html.fromstring(target_html)
                article_list = root.cssselect('.list_content .list_title a') #どうしてリストとして取得されるのだろうか。
                for a in article_list:
                    url = a.attrib['href'] #記事のurl
                    title = a.text_content #記事のタイトル
                    training_data.append({'url':url,'title':title,'category':category})
        return training_data

            
                
        
    def count(self,training_data): #training_data(カテゴリ、urlが辞書になったデータのリスト)からカテゴリーの頻度、カテゴリー別の単語の頻度を算出
        for d in training_data:
            cat = d['category']
            words = extract_words(d['url']) #training_dataは要素が辞書型なリスト型を想定
            self.catcount[cat] += 1
            for word in words:
                if word in self.wordcount[cat]: #そのカテゴリーでその単語は既に出ているか？
                    self.wordcount[cat][word] += 1 
                else:
                    self.wordcount[cat][word] = 1
                
                
    def prior_prob(self,cat): #カテゴリの事前確率
        num_of_training_data = 0
        for cat in self.categories:
            num_of_training_data += self.catcount[cat]
        return self.catcount[cat] / num_of_training_data
        
        

    def train(self):#各カテゴリの事前確率と、カテゴリ別の単語の登場頻度の辞書データをシリアライズ
        training_data = self.make_trainig_data()
        self.count(training_data)
        prior_probs = {}#各カテゴリの事前確率
        for cat in self.categories:
            prior_probs[cat] = self.prior_prob(cat)

        return self.wordcount,self.catcount,prior_probs
    
    
t = Training()
wordcount,catcount,priorprobs = t.train()

BASE = os.path.dirname(os.path.abspath(__file__))

        
with open(os.path.join(BASE,'word_count.pickle'), mode='wb') as w:
    pickle.dump(wordcount, w)
with open(os.path.join(BASE,'cat_count.pickle'), mode='wb') as c:
    pickle.dump(catcount, c)
with open(os.path.join(BASE,'prior_probs.pickle'), mode='wb') as p:
    pickle.dump(priorprobs, p)
            

print('Training done')