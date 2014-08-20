# -*- coding: utf-8 -*-
"""
    test_build_base
    ~~~~~~~~~~~~~~~

    Test the base build process.

    :copyright: Copyright 2007-2014 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import shutil

from nose.tools import with_setup

from util import test_roots, with_app, find_files

root = test_roots / 'test-intl'
build_dir = root / '_build'
locale_dir = build_dir / 'locale'


def setup_test():
    # Delete remnants left over after failed build
    locale_dir.rmtree(True)
    # copy all catalogs into locale layout directory
    for po in find_files(root, '.po'):
        copy_po = (locale_dir / 'en' / 'LC_MESSAGES' / po)
        if not copy_po.parent.exists():
            copy_po.parent.makedirs()
        shutil.copy(root / po, copy_po)


def teardown_test():
    build_dir.rmtree(True),


@with_setup(setup_test, teardown_test)
@with_app(buildername='html', srcdir=root,
          confoverrides={'language': 'en', 'locale_dirs': [locale_dir]})
def test_compile_all_catalogs(app):
    app.builder.compile_all_catalogs()

    catalog_dir = locale_dir / app.config.language / 'LC_MESSAGES'
    expect = set([
        x.replace('.po', '.mo')
        for x in find_files(catalog_dir, '.po')
    ])
    actual = set(find_files(catalog_dir, '.mo'))
    assert actual  # not empty
    assert actual == expect


@with_setup(setup_test, teardown_test)
@with_app(buildername='html', srcdir=root,
          confoverrides={'language': 'en', 'locale_dirs': [locale_dir]})
def test_compile_specific_catalogs(app):
    app.builder.compile_specific_catalogs(['admonitions'])

    catalog_dir = locale_dir / app.config.language / 'LC_MESSAGES'
    actual = set(find_files(catalog_dir, '.mo'))
    assert actual == set(['admonitions.mo'])


@with_setup(setup_test, teardown_test)
@with_app(buildername='html', srcdir=root,
          confoverrides={'language': 'en', 'locale_dirs': [locale_dir]})
def test_compile_update_catalogs(app):
    app.builder.compile_update_catalogs()

    catalog_dir = locale_dir / app.config.language / 'LC_MESSAGES'
    expect = set([
        x.replace('.po', '.mo')
        for x in find_files(catalog_dir, '.po')
    ])
    actual = set(find_files(catalog_dir, '.mo'))
    assert actual  # not empty
    assert actual == expect
