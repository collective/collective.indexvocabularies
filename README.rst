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

This package creates dynamic vocabularies based on any index in plone.

Typical use case for this is to provide a 'tags' type field.

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

To create a vocabulary from an index, go to the 'Index Vocabularies' control
panel and select the indexes you wish to create vocabularies for.

To use the vocabulary in a tag field, you will need to edit the XML Schema of
your content type. Currently this is only possible via the Classic UI
(Control Panel -> Content Types -> Schema -> Edit XML Schema)

A basic schema (without tag fields):

```
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

```
    <form:widget type="collective.indexvocabularies.widgets.TagSelectWidget">
        <vocabulary>collective.indexvocabularies.category</vocabulary>
    </form:widget>
```

The combined schema code would look like this:

```
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
