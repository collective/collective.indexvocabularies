from collective.indexvocabularies.vocabulary import IndexVocabulary
from plone import api
from plone.app.querystring.interfaces import IQueryField
from plone.registry import field
from plone.registry.record import Record
from zope.component import getSiteManager
from zope.interface.interfaces import ComponentLookupError
from zope.schema.interfaces import IVocabularyFactory

import logging


log = logging.getLogger("collective.indexvocabularies")
PREFIX = "plone.app.querystring.field"


def _create_index_vocabulary(index):
    """Registers a local vocabulary"""
    portal = api.portal.get()
    lsm = getSiteManager(portal)
    lsm.registerUtility(
        IndexVocabulary(index),
        IVocabularyFactory,
        name=f"collective.indexvocabularies.{index}",
    )


def _remove_index_vocabulary(index):
    """Removes a vocabulary"""
    portal = api.portal.get()
    lsm = getSiteManager(portal)
    try:
        util = lsm.getUtility(
            IVocabularyFactory, name=f"collective.indexvocabularies.{index}"
        )
    except ComponentLookupError:
        log.warn(
            f"Removing vocabulary failed: No vocabulary registered for collective.indexvocabularies.{index}"
        )
        return
    result = lsm.unregisterUtility(
        util, IVocabularyFactory, name=f"collective.indexvocabularies.{index}"
    )
    if result:
        log.warn(f"Could not remove vocabulary: collective.indexvocabularies.{index}")


def _sync_index_vocabularies():
    """Function to ensure that the local vocabularies match what is in the registry"""
    portal = api.portal.get()
    lsm = getSiteManager(portal)
    registry_values = api.portal.get_registry_record(
        "indexvocabularies.indexes", default=set()
    )
    vocabs = [
        i[0].split(".")[-1]
        for i in lsm.getUtilitiesFor(IVocabularyFactory)
        if i[0].startswith("collective.indexvocabularies.")
        and i[0] != "collective.indexvocabularies.KeywordIndexes"
    ]

    # Remove vocabs that shouldn't be there
    for vocab in list(set(vocabs) - set(registry_values)):
        log.warn(
            f"Vocabulary: collective.indexvocabularies.{vocab} is registered but not in the registry. Deleting"
        )
        _remove_index_vocabulary(vocab)

    # Add vocabs that are missing
    for vocab in list(set(registry_values) - set(vocabs)):
        log.warn(
            f"Vocabulary: collective.indexvocabularies.{vocab} is not registered. Registering"
        )
        _create_index_vocabulary(vocab)


def _list_index_vocabularies():
    """Function to ensure that the local vocabularies match what is in the registry"""
    portal = api.portal.get()
    lsm = getSiteManager(portal)
    vocabs = [
        i[0].split(".")[-1]
        for i in lsm.getUtilitiesFor(IVocabularyFactory)
        if i[0].startswith("collective.indexvocabularies.")
        and i[0] != "collective.indexvocabularies.KeywordIndexes"
    ]
    return vocabs


def _create_querystring_registry(index):
    """Registers the querystring values for the given index"""
    registry = api.portal.get_tool("portal_registry")
    registry.registerInterface(IQueryField, prefix=f"{PREFIX}.{index}")
    registry.records[f"{PREFIX}.{index}.title"] = Record(
        field.TextLine(title="Title"), index
    )
    registry.records[f"{PREFIX}.{index}.description"] = Record(
        field.Text(title="Description"), ""
    )
    registry.records[f"{PREFIX}.{index}.fetch_vocabulary"] = Record(
        field.Bool(title="Fetch vocabulary"), True
    )
    registry.records[f"{PREFIX}.{index}.enabled"] = Record(
        field.Bool(title="Enabled"), True
    )
    registry.records[f"{PREFIX}.{index}.group"] = Record(
        field.Text(title="Group"), "Metadata"
    )
    registry.records[f"{PREFIX}.{index}.operations"] = Record(
        field.List(title="Operations", value_type=field.TextLine()),
        [
            "plone.app.querystring.operation.selection.any",
            "plone.app.querystring.operation.selection.all",
            "plone.app.querystring.operation.selection.none",
        ],
    )
    registry.records[f"{PREFIX}.{index}.sortable"] = Record(
        field.Bool(title="Sortable"), False
    )
    registry.records[f"{PREFIX}.{index}.vocabulary"] = Record(
        field.TextLine(title="Vocabulary"), f"collective.indexvocabularies.{index}"
    )
    registry.records[f"{PREFIX}.{index}.indexvocabularies"] = Record(
        field.Bool(
            title="IndexVocabularies",
            description="Created by collective.indexvocabularies",
        ),
        True,
    )


def _remove_querystring_registry(index):
    """Removes the querystring registry entries for the given index"""
    registry = api.portal.get_tool("portal_registry")
    for x in [
        "title",
        "description",
        "fetch_vocabulary",
        "enabled",
        "group",
        "operations",
        "sortable",
        "vocabulary",
        "indexvocabularies",
    ]:
        del registry.records[f"{PREFIX}.{index}.{x}"]


def _sync_querystring_registry():
    """Function to ensure that the querystring registry entries are in sync"""
    registry = api.portal.get_tool("portal_registry")
    registry_values = api.portal.get_registry_record(
        "indexvocabularies.indexes", default=set()
    )
    fields = []
    qsfields = registry.records.values(PREFIX, IQueryField.__identifier__)
    for qsfield in qsfields:
        # Check to see if we have set our extra field
        if ".indexvocabularies>" in str(qsfield):
            fields.append(str(qsfield).split(".")[-2])
    for index in list(set(fields) - set(registry_values)):
        _remove_querystring_registry(index)

    for index in list(set(registry_values) - set(fields)):
        _create_querystring_registry(index)
