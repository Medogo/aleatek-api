from mission.models import ArticleSelect, Article, ArticleMission
from RICT.models import Disposition, AvisArticle, CommentaireAvisArticle
from django.forms.models import model_to_dict

def convert_to_dict(obj):
    result = {}

    for key, value in obj.items():
        if '[' in key and ']' in key:
            keys = key.split('[')
            keys = [k.strip(']') for k in keys if k.strip(']') != '']
            current_dict = result

            for i, k in enumerate(keys):
                if k not in current_dict:
                    current_dict[k] = {}

                if i == len(keys) - 1:
                    current_dict[k] = value
                else:
                    current_dict = current_dict[k]
        else:
            result[key] = value

    return result

def getllFirstParentOfArticle(articles):
    data = []
    for article in articles:
        while article.parent != None:
            article = article.parent
        data.append(article)
        
    return data

def getSubAffaireChild(article, mission):
    data = {
        'parent' : model_to_dict(article),
        'childs' : []
    }
    
    all_childs = Article.objects.filter(article_parent=article.id)
    
    for child in all_childs:
        if ArticleMission.objects.filter(article=child, mission=mission).exists():
            data['childs'].append(getSubAffaireChild(child, mission))
        
    return data

def getParentAffaire(article):
    
    if article['parent']['article_parent'] != None:    
        data = {
            'parent' : model_to_dict(Article.objects.get(id=article['parent']['article_parent'])),
            'childs' : [article]
        }
        return getParentAffaire(data)
    else:
        return article