from collective.indexvocabularies.utils import _list_index_vocabularies
from Products.Five.browser import BrowserView
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

class AdminView(BrowserView):

    def __call__(self):
        self.vocabs = _list_index_vocabularies()


        vocab = self.request.get('vocab')
        self.vocabulary_values = None
        if vocab and vocab in self.vocabs:
            factory = getUtility(IVocabularyFactory, name=f"collective.indexvocabularies.{vocab}")
            self.vocabulary_values = factory(self.context).by_value.keys()

        return super(AdminView, self).__call__()