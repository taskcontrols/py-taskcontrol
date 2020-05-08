
from .sharedbase import SharedBase
from .concurrency import ConcurencyBase


class PluginsBase(SharedBase, ConcurencyBase):

    # add plugin to instance or shared
    def plugin_register(self, name, plugin_instance):
        pass

    # return plugin instance/module
    def plugin_create(self, name, plugin_instance):
        pass