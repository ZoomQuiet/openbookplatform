from django import template
from inspect import getargspec
from django.utils.functional import curry
from django.template.context import Context
from django.template import Node, TemplateSyntaxError

class EnhancedLibrary(template.Library):
    def simple_tag(self,func):
        (params, xx, xxx, defaults) = getargspec(func)

        class SimpleNode(Node):
            def __init__(self, vars_to_resolve):
                self.vars_to_resolve = vars_to_resolve

            def render(self, context):
                resolved_vars = [var.resolve(context) for var in self.vars_to_resolve]
                return func(*resolved_vars)

        compile_func = curry(enhanced_generic_tag_compiler, params, defaults, func.__name__, SimpleNode)
        compile_func.__doc__ = func.__doc__
        self.tag(func.__name__, compile_func)
        return func

    def inclusion_tag(self, file_name, context_class=Context, takes_context=False):
        def dec(func):
            (params, xx, xxx, defaults) = getargspec(func)
            if takes_context:
                if params[0] == 'context':
                    params = params[1:]
                else:
                    raise TemplateSyntaxError, "Any tag function decorated with takes_context=True must have a first argument of 'context'"

            class InclusionNode(Node):
                def __init__(self, vars_to_resolve):
                    self.vars_to_resolve = vars_to_resolve

                def render(self, context):
                    resolved_vars = [var.resolve(context) for var in self.vars_to_resolve]
                    if takes_context:
                        args = [context] + resolved_vars
                    else:
                        args = resolved_vars

                    dict = func(*args)

                    if not getattr(self, 'nodelist', False):
                        from django.template.loader import get_template
                        t = get_template(file_name)
                        self.nodelist = t.nodelist
                    return self.nodelist.render(context_class(dict))

            compile_func = curry(enhanced_generic_tag_compiler, params, defaults, func.__name__, InclusionNode)
            compile_func.__doc__ = func.__doc__
            self.tag(func.__name__, compile_func)
            return func
        return dec

def enhanced_generic_tag_compiler(params, defaults, name, node_class, parser, token):
    "Returns a template.Node subclass."
    bits = token.contents.split()[1:]
    bmax = len(params)
    def_len = defaults and len(defaults) or 0
    bmin = bmax - def_len
    if(len(bits) < bmin or len(bits) > bmax):
        if bmin == bmax:
            message = "%s takes %s arguments" % (name, bmin)
        else:
            message = "%s takes between %s and %s arguments" % (name, bmin, bmax)
        raise TemplateSyntaxError, message
    return node_class(map(parser.compile_filter, bits))
