"""
    sphinx.builders.dirhtml
    ~~~~~~~~~~~~~~~~~~~~~~~

    Directory HTML builders.

    :copyright: Copyright 2007-2019 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from os import path

from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.deprecation import RemovedInSphinx40Warning, deprecated_alias
from sphinx.util import logging
from sphinx.util.osutil import SEP, os_path

if False:
    # For type annotation
    from typing import Any, Dict, Set  # NOQA
    from sphinx.application import Sphinx  # NOQA

logger = logging.getLogger(__name__)


class DirectoryHTMLBuilder(StandaloneHTMLBuilder):
    """
    A StandaloneHTMLBuilder that creates all HTML pages as "index.html" in
    a directory given by their pagename, so that generated URLs don't have
    ``.html`` in them.
    """
    name = 'dirhtml'

    def get_target_uri(self, docname, typ=None):
        # type: (str, str) -> str
        if docname == 'index':
            return ''
        if docname.endswith(SEP + 'index'):
            return docname[:-5]  # up to sep
        return docname + SEP

    def get_outfilename(self, pagename):
        # type: (str) -> str
        if pagename == 'index' or pagename.endswith(SEP + 'index'):
            outfilename = path.join(self.outdir, os_path(pagename) +
                                    self.out_suffix)
        else:
            outfilename = path.join(self.outdir, os_path(pagename),
                                    'index' + self.out_suffix)

        return outfilename

    def prepare_writing(self, docnames):
        # type: (Set[str]) -> None
        super().prepare_writing(docnames)
        self.globalcontext['no_search_suffix'] = True


# for compatibility
deprecated_alias('sphinx.builders.html',
                 {
                     'DirectoryHTMLBuilder': DirectoryHTMLBuilder,
                 },
                 RemovedInSphinx40Warning)


def setup(app):
    # type: (Sphinx) -> Dict[str, Any]
    app.setup_extension('sphinx.builders.html')

    app.add_builder(DirectoryHTMLBuilder)

    return {
        'version': 'builtin',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
