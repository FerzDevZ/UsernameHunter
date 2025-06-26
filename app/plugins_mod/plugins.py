# ...existing code from plugins.py...
def load_custom_platforms(custom_file=None):
    import json
    import os
    if not custom_file or not os.path.exists(custom_file):
        return {}
    with open(custom_file) as f:
        try:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

def load_plugin_platforms(plugin_dir='plugins'):
    import os
    import glob
    import importlib.util
    platforms = {}
    if not os.path.isdir(plugin_dir):
        return platforms
    for pyfile in glob.glob(os.path.join(plugin_dir, '*.py')):
        modulename = os.path.splitext(os.path.basename(pyfile))[0]
        if modulename.startswith('_'): continue
        spec = importlib.util.spec_from_file_location(modulename, pyfile)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, 'PLATFORM') and hasattr(mod, 'URL_PATTERN'):
            platforms[mod.PLATFORM] = mod.URL_PATTERN
    return platforms
