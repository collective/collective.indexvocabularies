from collective.indexvocabularies.interfaces import ITagSelectWidget
from plone.app.z3cform.widget import AjaxSelectWidget
from plone.autoform.widgets import WidgetExportImportHandler
from zope.interface import implementer_only
import collective.indexvocabularies.interfaces


@implementer_only(ITagSelectWidget)
class TagSelectWidget(AjaxSelectWidget):
    """Ajax select widget for z3c.form."""


TagSelectWidgetExportImportHandler = WidgetExportImportHandler(
    collective.indexvocabularies.interfaces.ITagSelectWidget
)
