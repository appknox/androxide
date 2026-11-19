"""androguard 4.1.3's module paths, with ``androguard`` renamed to
``androxide``, import and give the same objects as the short paths."""

import importlib
import subprocess
import sys

import pytest

# (androguard path, short path or None, names)
MIRRORED = [
    ("androxide.core.apk", "androxide.apk", ["APK", "FileNotPresent", "BrokenAPKError", "Error", "ARSCParser"]),
    ("androxide.core.dex", "androxide.dex",
     ["DEX", "EncodedMethod", "EncodedField", "ClassDefItem", "DalvikCode", "DCode", "Instruction", "Instruction35c",
      "Instruction11n", "Instruction21h", "Instruction21s", "Instruction31i", "InvalidInstruction"]),
    ("androxide.core.analysis.analysis", "androxide.analysis", ["Analysis", "ClassAnalysis", "MethodAnalysis"]),
    ("androxide.core.axml", "androxide.axml", ["AXMLPrinter", "ARSCParser", "ARSCResTableConfig"]),
    ("androxide.core.api_specific_resources", "androxide.api_specific_resources",
     ["load_permissions", "load_permission_mappings"]),
    ("androxide.core.androconf", None, ["load_api_specific_resource_module", "InvalidResourceError"]),
    ("androxide.misc", None, ["AnalyzeAPK"]),
    ("androxide.util", None, ["set_log"]),
    ("androxide.decompiler", None, []),
]


@pytest.mark.parametrize("path,short,names", MIRRORED, ids=[m[0] for m in MIRRORED])
def test_mirrored(path, short, names):
    mod = importlib.import_module(path)
    for name in names:
        assert getattr(mod, name) is not None
    if short is not None:
        assert mod is importlib.import_module(short)
        for name in names:
            assert getattr(mod, name) is getattr(importlib.import_module(short), name)


def test_import_forms():
    """The common androguard import forms, renamed, in a fresh
    interpreter, both import orders."""
    code = """
import sys
from androxide.core import apk
from androxide.core import api_specific_resources
from androxide.core import androconf
from androxide.core.apk import APK, FileNotPresent
from androxide.core.dex import DEX, EncodedMethod, ClassDefItem, Instruction, Instruction35c, DalvikCode, DCode
from androxide.core.dex import Instruction11n, Instruction21h, Instruction21s, Instruction31i
from androxide.core.analysis.analysis import Analysis, ClassAnalysis, MethodAnalysis
from androxide.core.axml import AXMLPrinter, ARSCParser
from androxide.util import set_log
from androxide.misc import AnalyzeAPK
import androxide.decompiler
import androxide.core.dex, androxide.dex, androxide.apk, androxide.axml, androxide.analysis
assert apk is androxide.apk and apk.APK is APK
assert androxide.core.dex is androxide.dex and androxide.dex.DEX is DEX
assert androxide.analysis.Analysis is Analysis
assert androxide.axml.ARSCParser is ARSCParser is androxide.apk.ARSCParser
assert sys.modules["androxide.core.dex"] is sys.modules["androxide.dex"]
assert sys.getrecursionlimit() == 5000
assert androconf.load_api_specific_resource_module("api_permission_mappings", 16)
assert "android.permission.INTERNET" in androconf.load_api_specific_resource_module("aosp_permissions", 99)
"""
    short_first = "import androxide.dex, androxide.apk, androxide.analysis, androxide.axml\n"
    for prefix in ("", short_first):
        subprocess.run([sys.executable, "-c", prefix + code], check=True)


def test_androconf_matches_androguard():
    ag = pytest.importorskip("androguard.core.androconf")
    from androxide.core import androconf

    for name in ("aosp_permissions", "api_permission_mappings"):
        for api in (None, 0, 3, 11, 16, "19", 20, 28, 34, 40):
            assert androconf.load_api_specific_resource_module(name, api) == \
                ag.load_api_specific_resource_module(name, api), (name, api)
    with pytest.raises(androconf.InvalidResourceError) as ours:
        androconf.load_api_specific_resource_module("nope")
    with pytest.raises(ag.InvalidResourceError) as theirs:
        ag.load_api_specific_resource_module("nope")
    assert str(ours.value) == str(theirs.value)
