# -*- coding: utf-8 -*-
from collective.indexvocabularies.vocabulary import IndexVocabularies
from plone import api
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform import directives as form
from plone.registry.interfaces import IRecordModifiedEvent
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.restapi.controlpanels.interfaces import IControlpanel
from plone.z3cform import layout
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form.browser.orderedselect import OrderedSelectWidget
from zope import event
from zope import schema
from zope.component import adapter
from zope.component import getSiteManager
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.interface import Interface
from zope.interface.interfaces import ComponentLookupError
from zope.schema.interfaces import IVocabularyFactory

_ = MessageFactory("collective.indexvocabularies")

def _create_index_vocabulary(index):
    portal = api.portal.get()
    lsm = getSiteManager(portal)
    lsm.registerUtility(IndexVocabularies(index), IVocabularyFactory, name=f'collective.indexvocabularies.{index}')

def _remove_index_vocabulary(index):
    portal = api.portal.get()
    lsm = getSiteManager(portal)
    try:
        util = lsm.getUtility(IVocabularyFactory, name=f'collective.indexvocabularies.{index}')
    except ComponentLookupError:
        return
    lsm.unregisterUtility(util, IVocabularyFactory, name=f'collective.indexvocabularies.{index}')
    return


class IIndexVocabulariesControlPanel(Interface):
    """ Control panel schema for the index vocabulary package"""

    #form.widget('indexes',
    #            OrderedSelectWidget,
    #            frontendOptions={"widget": "array"})
    indexes = schema.Set(
        title="Indexes to create vocabularies from",
        required=False,
       #vocabulary='collective.indexvocabularies.KeywordIndexes'
        value_type=schema.Choice(
            vocabulary='collective.indexvocabularies.KeywordIndexes'
        )
    )
    #indexes = schema.Text(required=False)


@adapter(Interface, Interface)
class IndexVocabulariesControlPanel(RegistryConfigletPanel):
    """ Control panel class for the index vocabulary package"""
    schema = IIndexVocabulariesControlPanel
    schema_prefix = "indexvocabularies"
    configlet_id = "indexvocabularies-controlpanel"
    configlet_category_id = "Products"
    title = "Index Vocabulary Settings"
    group = "Products"

def record_save(self):
    """ Event listener on plone.registry.interfaces.IRecordModifiedEvent """

    # TODO: Only trigger when collective.indexvocabularies is modified
    new_vals = [i for i in self.newValue if i not in self.oldValue]
    del_vals = [i for i in self.oldValue if i not in self.newValue]
    for index in new_vals:
        _create_index_vocabulary(index)
    for index in del_vals:
        _remove_index_vocabulary(index)
