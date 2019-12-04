from model import Article
from database import mysql as db
from recommend import Recommender


def get_by_id(aid: int):
    article = Article()

    entry, err = db.get_article_by_aid(aid)
    if not entry:
        return article
    article.id = entry['article_id']
    article.title = entry['title']
    article.authors = entry['authors']
    article.abstract = entry['abstract']

    entries = db.get_entries_by_aid(aid)
    for item in entries:
        article.journals.append(item['journal_id'])
        article.entries.append((item['link'], item['journal_name']))
    for journal in article.journals:
        fields = db.get_field_by_jid(journal)
        for field in fields:
            article.fields.add(field)
    return article


def title_search(query_str):
    results = db.article_title_search(query_str)
    return results


def full_search(query_str):
    results = db.article_full_search(query_str)
    return results


def lemma_search(query_str):
    ids = Recommender.lemma_search(query_str)
    results = db.get_title_by_aids(ids)
    return results


def list():
    return db.get_aid_title()
