# -*- coding: utf-8 -*-
from collective.indexvocabularies.utils import _sync_index_vocabularies
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "collective.indexvocabularies:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["collective.indexvocabularies.upgrades"]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""

    # Remove any registry entries
    if api.portal.get_registry_record('indexvocabularies.indexes', default=None) is not None:
        api.portal.set_registry_record('indexvocabularies.indexes', set([]))

    # Remove any vocabulary utilities
    _sync_index_vocabularies()
