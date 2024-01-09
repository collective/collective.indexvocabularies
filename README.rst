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


To create a custom tag field on a content type you will need to do the following

- Create a new field of type "Multiselect"
- Save the content type. This will create an index for this field.
- Go to Dynamic Vocabularies in the control panel
- Select the Index matching the field you just created and click "Make Vocabulary".
- Copy the name of the vocabulary generated.
- Edit your content type again but this time via the editing it's XML
  - Currently this is only possible via the Classic UI (Control Panel -> Content Types -> Schema -> Edit XML Schema)
- Change the widget to a TagSelectWidget with the vocabulary name that was generated.


For example:

```xml
  <field name="test" type="zope.schema.Set">
    <title>test</title>
    <value_type type="zope.schema.TextLine" />
    <form:widget type="collective.indexvocabularies.widgets.TagSelectWidget">
        <vocabulary>collective.dynamicvocabularies.uniquevalues.test</vocabulary>
    </form:widget>
  </field>
```


A basic schema (without tag fields):

```xml
  <model xmlns="http://namespaces.plone.org/supermodel/schema">
    <schema>
      <field name="test" type="zope.schema.Set">
        <title>test</title>
        <value_type type="zope.schema.TextLine" />
      </field>
    </schema>
  </model>
```

In order to make the field a 'tag' field, you will add the following widget
directive:

```xml
      <form:widget type="collective.indexvocabularies.widgets.TagSelectWidget">
          <vocabulary>collective.indexvocabularies.category</vocabulary>
      </form:widget>
```

The combined schema code would look like this:

```xml
  <model xmlns="http://namespaces.plone.org/supermodel/schema">
    <schema>
      <field name="test" type="zope.schema.Set">
        <title>test</title>
        <value_type type="zope.schema.TextLine" />
        <form:widget type="collective.indexvocabularies.widgets.TagSelectWidget">
            <vocabulary>collective.indexvocabularies.category</vocabulary>
        </form:widget>
      </field>
    </schema>
  </model>
```

You should now have a tags field configured on your content type.

Note that the tag field should be configured to use the same index that is
being read from. For example, you could create an index called 'categories',
which is mapped to the `Object.categories` field, then enable it in the
index vocabularies control panel. Once you have updated the schema to use the
new vocabulary you will have tags field that you can add values to.

Authors
-------

Jon Pentland, PretaGov Ltd - [instification]


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
