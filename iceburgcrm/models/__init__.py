import pkgutil
import importlib

import_errors = []

for loader, module_name, is_pkg in pkgutil.iter_modules(__path__, prefix=__name__ + '.'):
    if not is_pkg:
        try:
            module = importlib.import_module(module_name)
            for name in dir(module):
                attribute = getattr(module, name)
                if isinstance(attribute, type):
                    globals()[name] = attribute
        except ImportError as e:
            import_errors.append((module_name, str(e)))


if import_errors:
    for mod, err in import_errors:
        print(f"Failed to import {mod}: {err}")
