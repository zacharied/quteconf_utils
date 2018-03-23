# Xorg-related functionality.

__xres = None
__xres_namespace = '*'

from enum import Enum

class Color(Enum):
    BLACK   = 0
    RED     = 1
    GREEN   = 2
    YELLOW  = 3
    BLUE    = 4
    MAGENTA = 5
    CYAN    = 6
    WHITE   = 7
    BG      = 16
    FG      = 17

def _init_xresources():
    """Gets the local X resource database as a dictionary."""
    import subprocess

    xres = subprocess.run(['xrdb', '-query'], stdout=subprocess.PIPE)
    lines = xres.stdout.decode().split('\n')
    props = {}
    for line in filter(lambda l : l.startswith(__xres_namespace), lines):
        prop, _, value = line.partition(':\t')
        props[prop] = value
    return props

def set_xresources_namespace(name):
    """Sets the xrdb namespace used when accessing X resources."""
    global __xres
    global __xres_namespace

    __xres_namespace = name

    # Reload Xresources if they have already been loaded.
    if __xres:
        __xres = _init_xresources()

def xcolor(col, bright=False, alpha=1.0):
    """Gets a color from the X resources database."""
    
    # Load Xresources if necessary.
    global __xres
    if not __xres:
        __xres = _init_xresources() 

    # Check arguments.
    if (col == Color.BG or col == Color.FG) and bright == True:
        raise ValueError("cannot get bright color of background or foreground")

    if col == Color.BG:
        return __xres['*background']
    elif col == Color.FG:
        return __xres['*foreground']
    c_num = col.value if bright==False else col.value + 8
    return __xres['*color' + str(c_num)]
