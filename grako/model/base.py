""" Base definitions for models of programs.
"""
from ..rendering import Renderer

EOLCOL = 50

def render(node, **kwargs):
    """ Convert the given node to it's Java representation.
    """
    if node is None:
        return ''
    elif node is True:
        return 'true'
    elif node is False:
        return 'false'
    elif isinstance(node, list):
        return ''.join(render(e, **kwargs) for e in node)
    else:
        return str(node)

def indent(text, indent=1):
    """ Indent the given block of text by indent*4 spaces
    """
    if text is None:
        return ''
    text = str(text)
    if indent >= 0:
        lines = [' ' * 4 * indent + t for t in text.split('\n')]
        # check that a trailing EOL is not indented
#        if lines and not lines[-1].strip():
#            lines[-1] = ''
        text = '\n'.join(lines)
    return text

def rate(obj):
    """ Rate the given tree negatively for each node that is a generic Node
    """
    result = 0
    if isinstance(obj, Node):
        result += -1 * (obj.__class__ == Node)
        result += sum(rate(c) for c in obj.children)
    if isinstance(obj, list):
        result += sum(rate(e) for e in obj)
    return result


class Context(object):
    """ Context for source code generation.

        It contains a copy of the source code when available,
        a symbol table, and a stack of active views for symbols
        that are used anonymously.
    """

    def __init__(self, buf, eol_comments=True):
        super(Context, self).__init__()
        self.buf = buf
        self.eol_comments = eol_comments

        self._symbols = dict()



class Node(Renderer):
    """ Base class for model nodes, in charge of the rendering infrastructure.

        Rendering consists of providing arguments through object attributes
        and the :meth:render_fields method for them to be applied to a
        :class:`string.Template` instance created from the *template* class
        variable.
    """

    inline = True
    template = '$name'

    def __init__(self, ctx, parseinfo=None):
        super(Node, self).__init__()
        self._ctx = ctx
        self._parseinfo = parseinfo

    @property
    def ctx(self):
        return self._ctx


    def __str__(self):
        return self.render()
