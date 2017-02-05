from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from cms.models import Article
from cms.forms import ArticleForm, UrlForm
from classifier.classifier import Classifier  # @UnresolvedImport


def article_list(request):
    """記事の一覧"""

    articles = Article.objects.all().order_by('id')
    return render(request,
                  'cms/article_list.html',     # 使用するテンプレート
                  {'articles': articles})         # テンプレートに渡すデータ


def article_edit(request, article_id=None):
    """記事の編集"""
    if article_id:   # article_id が指定されている (修正時)
        article = get_object_or_404(Article, pk=article_id)

        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():    # フォームのバリデーション
                article = form.save(commit=False)
                article.save()
                return redirect('cms:article_list')
        else:    # GET の時
            form = ArticleForm(instance=article)

    else:         # article_id が指定されていない (追加時)
        article = Article()

        if request.method == 'POST':
            form = UrlForm(request.POST)
            if form.is_valid():  # フォームのバリデーション
                url = form.cleaned_data['article_url']
                title, url, category = Classifier().classify(
                    url)  # データベースの追加をしてから値も返す。
                Classifier().save_article(title, url, category)
                return render(request, 'cms/article_new.html',
                              dict(title=title, url=url, category=category))

        # GET の時←「追加」ボタンを押して最初に行く画面のことか？であれば、UrlFormを生成してtemplateのhtmlに渡す。
        else:
            form = UrlForm()

    return render(request, 'cms/article_edit.html',
                  dict(form=form, article_id=article_id))


def article_del(request, article_id):
    """記事の削除"""
    article = get_object_or_404(Article, pk=article_id)
    article.delete()
    return redirect('cms:article_list')
