"""
Tests for nested class indexing feature.

Run: python tests/test_nested_class_indexing.py
"""
import sys
import os

# Add harmony-api/scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'skills', 'harmony-api', 'scripts'))

from sdk_indexer import SDKIndexer, NestedClass, ClassInfo
from check_sdk_imports import find_sdk_home


def get_sdk_or_fail():
    """Get SDK home or fail the test."""
    sdk_home = find_sdk_home()
    if not sdk_home:
        raise RuntimeError("SDK not found: set DEVECO_SDK_HOME or ensure hdc is in PATH")
    return sdk_home


def get_or_build_index(sdk_home: str, index_path: str) -> SDKIndexer:
    """Get indexer, building if needed."""
    indexer = SDKIndexer(sdk_home=sdk_home, index_path=index_path)
    if indexer.needs_rebuild():
        indexer.build_index()
        indexer.save()
    else:
        indexer.load()
    return indexer


def test_nested_class_dataclass():
    """Test NestedClass dataclass creation and fields."""
    nc = NestedClass(
        parent_module="@ohos.web.webview",
        namespace="webview",
        class_name="WebviewController",
        members=["load", "refresh"],
        statics=[]
    )
    assert nc.parent_module == "@ohos.web.webview"
    assert nc.namespace == "webview"
    assert nc.class_name == "WebviewController"
    assert "load" in nc.members
    assert "refresh" in nc.members
    print("PASS: test_nested_class_dataclass")


def test_parse_dts_file_returns_tuple():
    """Test that _parse_dts_file returns (ModuleInfo, List[NestedClass])."""
    sdk_home = get_sdk_or_fail()
    indexer = SDKIndexer(sdk_home=sdk_home, index_path=".sdk_index.json")
    dts_file = os.path.join(sdk_home, "openharmony/ets/api/@ohos.web.webview.d.ts")
    result = indexer._parse_dts_file(dts_file)
    assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
    assert len(result) == 2, f"Expected 2 elements, got {len(result)}"
    module_info, nested_classes = result
    assert isinstance(nested_classes, list), f"Expected list, got {type(nested_classes)}"
    webcontroller_nc = next(
        (nc for nc in nested_classes if nc.class_name == "WebviewController"),
        None
    )
    assert webcontroller_nc is not None, "WebviewController not found in nested classes"
    assert "load" in webcontroller_nc.members or len(webcontroller_nc.members) > 0
    print(f"PASS: test_parse_dts_file_returns_tuple (found {len(nested_classes)} nested classes)")


def test_build_index_creates_synthetic_modules():
    """Test that build_index creates synthetic modules for nested classes."""
    sdk_home = get_sdk_or_fail()
    indexer = SDKIndexer(sdk_home=sdk_home, index_path=".sdk_index_test.json")
    indexer.build_index()

    synthetic_path = "@ohos.web.webview.webview.WebviewController"
    assert synthetic_path in indexer.modules, f"Synthetic module {synthetic_path} not found"

    synthetic_mod = indexer.modules[synthetic_path]
    assert "WebviewController" in synthetic_mod.classes, "WebviewController class not in synthetic module"

    if os.path.exists(".sdk_index_test.json"):
        os.remove(".sdk_index_test.json")
    print("PASS: test_build_index_creates_synthetic_modules")


def test_query_nested_class_members():
    """Test querying members of nested class via module path."""
    sdk_home = get_sdk_or_fail()
    indexer = get_or_build_index(sdk_home, ".sdk_index.json")

    synthetic_path = "@ohos.web.webview.webview.WebviewController"
    mod = indexer.get(synthetic_path)
    assert mod is not None, f"Could not get module {synthetic_path}"

    cls = mod.classes.get("WebviewController")
    assert cls is not None, "WebviewController class not found"

    members_lower = [m.lower() for m in cls.members]
    assert any("load" in m for m in members_lower), "load method not found"
    assert any("refresh" in m for m in members_lower), "refresh method not found"

    print(f"PASS: test_query_nested_class_members ({len(cls.members)} members found)")


def test_nested_class_has_correct_export_type():
    """Test that nested classes have export_type='nested'."""
    sdk_home = get_sdk_or_fail()
    indexer = get_or_build_index(sdk_home, ".sdk_index.json")

    synthetic_path = "@ohos.web.webview.webview.WebviewController"
    mod = indexer.get(synthetic_path)
    assert mod is not None

    cls = mod.classes.get("WebviewController")
    assert cls is not None
    assert cls.export_type == "nested", f"Expected export_type='nested', got '{cls.export_type}'"

    print("PASS: test_nested_class_has_correct_export_type")


def test_query_no_duplicates():
    """Test that query results don't contain duplicates."""
    from check_sdk_imports import query_mode

    sdk_home = get_sdk_or_fail()
    indexer = get_or_build_index(sdk_home, ".sdk_index.json")

    results = query_mode("WebviewController", indexer)
    items = [r.item for r in results]

    assert len(items) == len(set(items)), f"Found duplicates: {[x for x in items if items.count(x) > 1]}"

    webcontroller_count = items.count("@ohos.web.webview.webview.WebviewController")
    assert webcontroller_count == 1, f"Expected 1, got {webcontroller_count}"

    print(f"PASS: test_query_no_duplicates ({len(items)} unique results)")


def test_query_nested_class_shows_members():
    """Test that querying nested class shows members directly."""
    from check_sdk_imports import query_mode

    sdk_home = get_sdk_or_fail()
    indexer = get_or_build_index(sdk_home, ".sdk_index.json")

    results = query_mode("@ohos.web.webview.webview.WebviewController", indexer)

    assert len(results) > 1, "Expected member listing"

    member_names = [r.item.strip() for r in results[1:]]
    assert "refresh" in member_names, "refresh member not found"
    assert "load" in member_names or "loadUrl" in member_names, "load member not found"

    print(f"PASS: test_query_nested_class_shows_members ({len(results)} results)")


def test_partial_match_member_not_module():
    """Test that querying a member name doesn't return fake module matches.

    webPageSnapshot is a member of WebviewController class, not a module.
    Partial match should not return fake modules like @ohos.web.webview.webview.webPageSnapshot.
    """
    from check_sdk_imports import query_mode

    sdk_home = get_sdk_or_fail()
    indexer = get_or_build_index(sdk_home, ".sdk_index.json")

    results = query_mode("webPageSnapshot", indexer)
    items = [r.item for r in results]

    # webPageSnapshot is a member name, not a module name
    # Should NOT see @ohos.web.webview.webview.webPageSnapshot as a result
    assert "@ohos.web.webview.webview.webPageSnapshot" not in items, \
        "webPageSnapshot should not be treated as a standalone module"

    # Should find @kit.ArkWeb.webview.webPageSnapshot (valid module member)
    assert "@kit.ArkWeb.webview.webPageSnapshot" in items, \
        f"@kit.ArkWeb.webview.webPageSnapshot not found. Results: {items}"

    print(f"PASS: test_partial_match_member_not_module ({len(items)} results)")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running nested class indexing tests...")
    print("=" * 60)

    test_nested_class_dataclass()
    test_parse_dts_file_returns_tuple()
    test_build_index_creates_synthetic_modules()
    test_query_nested_class_members()
    test_nested_class_has_correct_export_type()
    test_query_no_duplicates()
    test_query_nested_class_shows_members()
    test_partial_match_member_not_module()

    print("=" * 60)
    print("All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()