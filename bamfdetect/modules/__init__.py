import os
import glob
import importlib

__all__ = [ os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(os.path.abspath(__file__))+"/*.py")]
__all__ = [ v for v in __all__ if not v == "__init__" and not v == "bin_parse_module" ]

for mod in __all__:
    importlib.import_module("bamfdetect.modules." +  mod)