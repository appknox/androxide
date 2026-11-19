"""androxide: the native module (DEX index, resources, binary XML, zip),
re-exported here, plus pure-Python drop-ins for androguard 4.1.3's modules,
under androguard's own paths (``androguard`` renamed to ``androxide``):

- ``androxide.core.apk``: ``APK``, ``FileNotPresent``, ...
- ``androxide.core.dex``: ``DEX``, ``ClassDefItem``, ``EncodedMethod``,
  ``DalvikCode``, ``DCode``, the ``Instruction*`` classes, ...
- ``androxide.core.analysis.analysis``: ``Analysis``, ``ClassAnalysis``,
  ``MethodAnalysis``
- ``androxide.core.axml``: ``AXMLPrinter``, ``ARSCParser``, ...
- ``androxide.core.api_specific_resources``: ``load_permissions``,
  ``load_permission_mappings``
- ``androxide.core.androconf``: ``load_api_specific_resource_module``
- ``androxide.misc``: ``AnalyzeAPK``
- ``androxide.util``: ``set_log``
- ``androxide.decompiler``: only the import's recursion-limit side effect

The short paths ``androxide.apk``, ``.dex``, ``.analysis``, ``.axml`` and
``.api_specific_resources`` are the same modules as their ``core`` paths.
"""

from . import androxide as _native
from .androxide import *  # noqa: F401,F403

# Private helpers (test hooks) too, so `androxide._x` keeps working.
for _k in dir(_native):
    if not _k.startswith("__"):
        globals()[_k] = getattr(_native, _k)
del _k
