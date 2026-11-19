"""``androguard.core``: androguard 4.1.3's module paths over this package.

``androxide.core.apk``, ``.dex``, ``.axml``, ``.api_specific_resources``
and ``.analysis.analysis`` are the modules ``androxide.apk``, ``.dex``,
``.axml``, ``.api_specific_resources`` and ``.analysis`` themselves (the same
module objects, so the same classes), registered under androguard's names when
first imported. ``androxide.core.androconf`` provides
``load_api_specific_resource_module``. Code written against androguard
switches by renaming ``androguard`` to ``androxide`` in its imports.
"""
