import lxml.html  # @UnresolvedImport
import requests
from janome.tokenizer import Tokenizer


def get_title(target_url):
    target_html = requests.get(target_url).text
    root = lxml.html.fromstring(target_html)
    return root.cssselect('.article_header_title')[0].text_content()


def get_body(target_url):
    target_html = requests.get(target_url).text
    root = lxml.html.fromstring(target_html)
    return root.cssselect('.article')[0].text_content()


def extract_words(url): #urlから単語のセットを作る
    words = set()
    t = Tokenizer()
    tokens = t.tokenize(get_body(url)) ##本文をスクレイピングしtokensに形態素解析結果を格納
    
    #名詞だけを取り出す
    for token in tokens:            
        partOfSpeech = token.part_of_speech.split(',')[0] # 品詞を取り出し
        if partOfSpeech == '名詞':
            words.add(token.surface)
    return words

