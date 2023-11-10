from collective.indexvocabularies.vocabulary import IndexVocabulary
from plone import api
from zope.component import getSiteManager
from zope.interface.interfaces import ComponentLookupError
from zope.schema.interfaces import IVocabularyFactory

import logging


log = logging.getLogger('collective.indexvocabularies')

def _create_index_vocabulary(index):
    """ Registers a local vocabulary """
    portal = api.portal.get()
    lsm = getSiteManager(portal)
    lsm.registerUtility(IndexVocabulary(index), IVocabularyFactory, name=f'collective.indexvocabularies.{index}')

def _remove_index_vocabulary(index):
    """ Removes a vocabulary """
    log.info(f'Removing vocabulary collective.indexvocabularies.{index}')
    portal = api.portal.get()
    lsm = getSiteManager(portal)
    try:
        util = lsm.getUtility(IVocabularyFactory, name=f'collective.indexvocabularies.{index}')
    except ComponentLookupError:
        log.warn(f'Removing vocabulary failed: No vocabulary registered for collective.indexvocabularies.{index}')
        return
    result = lsm.unregisterUtility(util, IVocabularyFactory, name=f'collective.indexvocabularies.{index}')
    if result:
        log.warn(f'Could not remove vocabulary: collective.indexvocabularies.{index}')

def _sync_index_vocabularies():
    """ Function to ensure that the local vocabularies match what is in the registry"""
    portal = api.portal.get()
    lsm = getSiteManager(portal)
    registry_values = api.portal.get_registry_record('indexvocabularies.indexes', default=set())
    vocabs = [i[0].split('.')[-1] for i in
              lsm.getUtilitiesFor(IVocabularyFactory)
              if i[0].startswith('collective.indexvocabularies.')
              and i[0] != 'collective.indexvocabularies.KeywordIndexes']

    # Remove vocabs that shouldn't be there
    for vocab in list(set(vocabs) - set(registry_values)):
        log.warn(f'Vocabulary: collective.indexvocabularies.{vocab} is registered but not in the registry. Deleting')

    # Add vocabs that are missing
    for vocab in list(set(registry_values) - set(vocabs)):
        log.warn(f'Vocabulary: collective.indexvocabularies.{vocab} is not registered. Registering')
        _create_index_vocabulary(vocab)
