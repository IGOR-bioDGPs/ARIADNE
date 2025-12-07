import collections
import collections.abc

# --- Compatibility patch for pybtex / sphinxcontrib.apa ---
for attr in ("Mapping", "MutableMapping", "Sequence"):
    if not hasattr(collections, attr):
        setattr(collections, attr, getattr(collections.abc, attr))