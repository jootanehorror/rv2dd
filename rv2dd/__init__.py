import importlib as _importlib

def __getattr__(name):
     return _importlib.import_module(f'rv2dd.{name}')
