.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/collective.indexvocabularies/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/collective.indexvocabularies/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/collective.indexvocabularies/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/collective.indexvocabularies?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/collective.indexvocabularies/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/collective.indexvocabularies

.. image:: https://img.shields.io/pypi/v/collective.indexvocabularies.svg
    :target: https://pypi.python.org/pypi/collective.indexvocabularies/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.indexvocabularies.svg
    :target: https://pypi.python.org/pypi/collective.indexvocabularies
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.indexvocabularies.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.indexvocabularies.svg
    :target: https://pypi.python.org/pypi/collective.indexvocabularies/
    :alt: License


============================
collective.indexvocabularies
============================

A Plone addon for creating dynamic vocabularies from catalog indexes.

This package allows an admin to create dynamic named vocabularies from data within the plone site.
Vocabularies can then be used in metadata fields of your content types or in facets on a search block in volto.

Currently supported is making vocabularies from existing unique values of a metadata field. This is useful to create
a custom Tags field which is addable by editors, similar to the built in Subjects field.

Installation
------------

Install collective.indexvocabularies by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.indexvocabularies


and then running ``bin/buildout``

Activation
----------

Activate the add-on by installing it in the Addons Control panel.

Configure
---------


To add a custom tag field to your content type you will need to do the following:

- Go to the Content Types control panel
   - Create a new field of type "Multiselect"
   - Save the content type. This will create an index for this field.
- Go to the Dynamic Vocabularies control panel
   - Select the index dropdown and select the field you just created
   - Save the settings. This creates a vocabulary that is accessed via ``collective.indexvocabularies.{your_field_name}``
- Go to the Content Types control panel
   - Currently this is only possible via the Classic UI
   - Go to Content Types -> Schema and select "Edit XML Schema"
   - Change the widget to a TagSelectWidget with the vocabulary name that was generated (instructions below).

Example Fieldset (where the new field name is ``test``)::

  <model xmlns="http://namespaces.plone.org/supermodel/schema">
    <schema>
      <field name="test" type="zope.schema.Set">
        <title>test</title>
        <value_type type="zope.schema.TextLine" />
        <form:widget type="collective.indexvocabularies.widgets.TagSelectWidget">
            <vocabulary>collective.indexvocabularies.test</vocabulary>
        </form:widget>
      </field>
    </schema>
  </model>


Updating the XML Fieldset
=========================

A basic schema (without tag fields) looks like this::

  <model xmlns="http://namespaces.plone.org/supermodel/schema">
    <schema>
      <field name="test" type="zope.schema.Set">
        <title>test</title>
        <value_type type="zope.schema.TextLine" />
      </field>
    </schema>
  </model>

In order to make the field a 'tag' field, you will add the following widget
directive::

      <form:widget type="collective.indexvocabularies.widgets.TagSelectWidget">
          <vocabulary>collective.indexvocabularies.test</vocabulary>
      </form:widget>



The combined schema code would then be::

  <model xmlns="http://namespaces.plone.org/supermodel/schema">
    <schema>
      <field name="test" type="zope.schema.Set">
        <title>test</title>
        <value_type type="zope.schema.TextLine" />
        <form:widget type="collective.indexvocabularies.widgets.TagSelectWidget">
            <vocabulary>collective.indexvocabularies.test</vocabulary>
        </form:widget>
      </field>
    </schema>
  </model>


You should now have a tags field configured on your content type.


Authors
-------

Jon Pentland, PretaGov Ltd - [instification]
Dylan Jay, PretaGov Ltd - [djay]

Contribute
----------

- Issue Tracker: https://github.com/collective/collective.indexvocabularies/issues
- Source Code: https://github.com/collective/collective.indexvocabularies


Support
-------

If you are having issues, please create an issue in the GitHub repo.


License
-------

The project is licensed under the GPLv2.
