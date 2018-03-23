from . import yaml

__c = None
__config = None

def init(c, config):
    global __c
    global __config
    __c = c
    __config = config
