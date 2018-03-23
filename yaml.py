from . import xres

import yaml
import re
import ast

def __dict_attrs(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from __dict_attrs(v, '{}.{}'.format(path, k) if path else k)
    else:
        yield path, obj

def __is_int(s):
    """Helper function that returns whether or not a string textually
    represents an integer."""
    try:
        int(s)
        return True
    except ValueError:
        return False

# Gets a config value given a key in the match group.
def __regex_sub_ref(m):
    from . import __config
    return __config.get(m.group(1))

def __regex_sub_xcolor(m):
    return eval("xres.xcolor(xres.Color.{})".format(m.group(1)))

def config_from_yaml(name):
    """Given a YAML file, sets values in the qutebrowser config according to
    that file."""

    from . import __config

    # Regexes that define special cases in the YAML file.
    re_ref = re.compile(r'\$([A-Za-z]+(\.[A-Za-z]+)*)')
    re_xcolor = re.compile(r'\+X\((.+)\)')
    re_list = re.compile(r'\[.*\]')

    with (__config.configdir / 'yml' / '{}.yml'.format(name)).open() as f:
        yaml_data = yaml.load(f)
        for k, v in __dict_attrs(yaml_data): 
            v = str(v)
            v = re_ref.sub(__regex_sub_ref, v)
            v = re_xcolor.sub(__regex_sub_xcolor, v)

            if __is_int(v):
                __config.set(k, int(v))
            elif v == 'True':
                __config.set(k, True)
            elif v == 'False':
                __config.set(k, False)
            else:
                __config.set(k, ast.literal_eval(v) if re_list.match(v) else v)
