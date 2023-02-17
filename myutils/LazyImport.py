import importlib
class LazyImport(object):
    def __init__(self):
        self.cache = {}
    def __call__(self,modul_path):
        self.mod_name = modul_path
        return self
    def getRes(self,modul_path,name):
        return self.__call__(modul_path).__getattr__(name)
    def __getattr__(self, name):
        mod = self.cache.get(self.mod_name)
        if not mod:
            mod = importlib.import_module(self.mod_name)
            self.cache[self.mod_name] = mod
        return getattr(mod, name)
lazy_import = LazyImport()