from plone import api
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from plone.base.utils import safe_text
from Products.PluginIndexes.FieldIndex.FieldIndex import FieldIndex
from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def _get_keyword_indexes():
    results = []
    pc = api.portal.get_tool("portal_catalog")
    indexes = [i for i in pc.indexes()]
    for index in indexes:
        index = pc.Indexes[index]
        if index.__class__ != KeywordIndex and index.__class__ != FieldIndex:
            continue
        results.append(index.id)
    return results


def _get_index_values(index):
    pc = api.portal.get_tool("portal_catalog")
    index = pc.Indexes[index]
    return [i for i in index.uniqueValues()]


@provider(IVocabularyFactory)
def KeywordIndexesVocabularyFactory(context):
    values = _get_keyword_indexes()
    return safe_simplevocabulary_from_values(values)


@provider(IVocabularyFactory)
def index_vocabularies_factory(context):
    return


def IndexVocabulary(name):
    return IndexVocabularies(name).__call__


class IndexVocabularies:
    def __init__(self, name):
        self.name = name

    def __call__(self, context):
        values = _get_index_values(self.name)
        items = [
            SimpleTerm(value, safe_text(value), safe_text(value)) for value in values
        ]
        return SimpleVocabulary(items)
