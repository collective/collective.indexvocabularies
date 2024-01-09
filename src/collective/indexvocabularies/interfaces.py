# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.app.z3cform.interfaces import IAjaxSelectWidget
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.interfaces import IVocabularyFactory

import zope.schema


class ICollectiveIndexvocabulariesLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IIndexVocabulary(IVocabularyFactory):
    """ Interface for storing dynamic vocabularies """


class ITagSelectWidget(IAjaxSelectWidget):
    """Marker interface for the ITagSelectWidget."""

    pattern = zope.schema.TextLine(
        title='Pattern',
        default="select2"
    )

    pattern_options = zope.schema.Text(
        title='Pattern Options',
        default=''
    )

    separator = zope.schema.TextLine(
        title='Separator',
        default=";"
    )

    vocabulary = zope.schema.TextLine(
        title='Vocabulary',
        default=None
    )

    vocabulary_view = zope.schema.TextLine(
        title='Vocabulary View',
        default="@@getVocabulary"
    )

    orderable = zope.schema.Bool(
        title='Orderable',
        default=False
    )
