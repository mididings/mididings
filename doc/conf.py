# -*- coding: utf-8 -*-
#
import re

from sphinx.domains.python import PyFunction
from sphinx import addnodes

# project-specific configuration
project = "mididings"
copyright = "mididings contributors"
version = "20230114"

# general configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinxcontrib.fulltoc",
]
root_doc = "index"
exclude_patterns = ["build"]
templates_path = ["templates"]
add_module_names = False

# html configuration
html_theme = "nasophon"
html_theme_path = ["theme"]
html_copy_source = False

# extension configuration - autodoc
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
}


class DingsFunction(PyFunction):
    """
    Stripped-down version of the 'function::' directive that accepts an
    additional argument in angle brackets, used to specify the node's
    'fullname' attribute. This allows proper cross-references to mididings
    operators.
    """

    def handle_signature(self, sig, signode):
        m = re.match("(.*) <([\w.]*)>", sig)
        if m:
            op = m.group(1)
            name = m.group(2)
            modname = self.options.get("module", self.env.temp_data.get("py:module"))

            signode["module"] = modname
            signode["class"] = ""
            signode["fullname"] = name
            signode += addnodes.desc_name(op, op)

            return name, None
        else:
            return super(PyFunction, self).handle_signature(sig, signode)


def setup(app):
    app.add_directive("dingsfun", DingsFunction)
