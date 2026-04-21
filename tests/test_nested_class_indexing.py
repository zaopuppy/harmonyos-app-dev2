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
from report import Status


_global_indexer = None


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


def rebuild_index(sdk_home: str, index_path: str) -> SDKIndexer:
    """Force rebuild and return indexer."""
    indexer = SDKIndexer(sdk_home=sdk_home, index_path=index_path)
    indexer.build_index()
    indexer.save()
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
    dts_file = os.path.join(sdk_home, "default/openharmony/ets/api/@ohos.web.webview.d.ts")
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
    mod = _global_indexer.get("@ohos.web.webview.webview.WebviewController")
    assert mod is not None, "Could not get module @ohos.web.webview.webview.WebviewController"

    cls = mod.classes.get("WebviewController")
    assert cls is not None, "WebviewController class not found"

    members_lower = [m.lower() for m in cls.members]
    assert any("load" in m for m in members_lower), "load method not found"
    assert any("refresh" in m for m in members_lower), "refresh method not found"

    print(f"PASS: test_query_nested_class_members ({len(cls.members)} members found)")


def test_nested_class_has_correct_export_type():
    """Test that nested classes have export_type='nested'."""
    mod = _global_indexer.get("@ohos.web.webview.webview.WebviewController")
    assert mod is not None

    cls = mod.classes.get("WebviewController")
    assert cls is not None
    assert cls.export_type == "nested", f"Expected export_type='nested', got '{cls.export_type}'"

    print("PASS: test_nested_class_has_correct_export_type")


def test_query_no_duplicates():
    """Test that query results don't contain duplicates."""
    from check_sdk_imports import query_mode

    results = query_mode("WebviewController", _global_indexer)
    items = [r.item for r in results]

    assert len(items) == len(set(items)), f"Found duplicates: {[x for x in items if items.count(x) > 1]}"

    webcontroller_count = items.count("@ohos.web.webview.webview.WebviewController")
    assert webcontroller_count == 1, f"Expected 1, got {webcontroller_count}"

    print(f"PASS: test_query_no_duplicates ({len(items)} unique results)")


def test_query_nested_class_shows_members():
    """Test that querying nested class shows members directly."""
    from check_sdk_imports import query_mode

    results = query_mode("@ohos.web.webview.webview.WebviewController", _global_indexer)

    assert len(results) > 1, "Expected member listing"

    member_names = [r.item.strip() for r in results[1:]]
    assert "refresh" in member_names, "refresh member not found"
    assert "load" in member_names or "loadUrl" in member_names, "load member not found"

    print(f"PASS: test_query_nested_class_shows_members ({len(results)} results)")


def test_partial_match_member_not_module():
    """Test that partial match for member name returns correct results.

    When querying "webPageSnapshot", should find the member in its proper context,
    not fake module paths that don't actually exist.
    """
    from check_sdk_imports import query_mode

    results = query_mode("webPageSnapshot", _global_indexer)
    items = [r.item for r in results]

    # webPageSnapshot is a member of WebviewController, not a standalone module
    # Should NOT see these fake module paths in results:
    assert "@ohos.web.webview.webview.webPageSnapshot" not in items, \
        "webPageSnapshot should not be treated as @ohos.web.webview.webview.webPageSnapshot module"
    assert "@kit.ArkWeb.webview.webPageSnapshot" not in items, \
        "webPageSnapshot should not be treated as @kit.ArkWeb.webview.webPageSnapshot module"

    print(f"PASS: test_partial_match_member_not_module ({len(items)} results: {items[:3]})")

    print(f"PASS: test_partial_match_member_not_module ({len(items)} results)")


def test_query_member_no_duplicate_path():
    """Test that # query for nested class module doesn't produce duplicate paths.

    Querying @ohos.web.webview.webview.WebviewController#refresh should return
    @ohos.web.webview.webview.WebviewController#refresh (not WebviewController.WebviewController#refresh).
    """
    from check_sdk_imports import query_mode

    # Query existing member
    results = query_mode("@ohos.web.webview.webview.WebviewController#refresh", _global_indexer)
    assert len(results) == 1, f"Expected 1 result, got {len(results)}"

    # Should NOT have duplicate WebviewController.WebviewController
    assert "WebviewController.WebviewController" not in results[0].item, \
        f"Path should not duplicate class name: {results[0].item}"

    # Should be the correct path
    assert results[0].item == "@ohos.web.webview.webview.WebviewController#refresh", \
        f"Expected @ohos.web.webview.webview.WebviewController#refresh, got {results[0].item}"
    assert results[0].status == Status.OK, f"Expected OK status, got {results[0].status}"

    print(f"PASS: test_query_member_no_duplicate_path")


def test_query_result_has_filepath():
    """Test that query results include the .d.ts file path and line number."""
    from check_sdk_imports import query_mode

    # Uses _global_indexer rebuilt once at start
    results = query_mode("@ohos.web.webview.webview.WebviewController#refresh", _global_indexer)
    assert len(results) == 1, f"Expected 1 result, got {len(results)}"

    # Should have a file_path
    assert results[0].file_path, "file_path should not be empty"
    assert "@ohos.web.webview.d.ts" in results[0].file_path, \
        f"Expected file_path to contain @ohos.web.webview.d.ts, got {results[0].file_path}"

    # Should have correct line number (WebviewController is at line 3579)
    assert results[0].line_number == 3579, \
        f"Expected line_number=3579, got {results[0].line_number}"

    print(f"PASS: test_query_result_has_filepath ({results[0].file_path}:{results[0].line_number})")


def test_partial_query_result_has_filepath():
    """Test that partial member queries include the .d.ts file path and line number."""
    from check_sdk_imports import query_mode

    sdk_home = get_sdk_or_fail()
    indexer = get_or_build_index(sdk_home, ".sdk_index.json")

    results = query_mode("webPageSnapshot", indexer)
    assert len(results) >= 1, "Expected at least one partial query result"

    target = next(
        (r for r in results if r.item == "@ohos.web.webview.webview.WebviewController#webPageSnapshot"),
        None
    )
    assert target is not None, "Expected webPageSnapshot member result"
    assert target.file_path, "file_path should not be empty for partial member query"
    assert "@ohos.web.webview.d.ts" in target.file_path, \
        f"Expected file_path to contain @ohos.web.webview.d.ts, got {target.file_path}"
    assert target.line_number == 3579, \
        f"Expected line_number=3579, got {target.line_number}"

    print(f"PASS: test_partial_query_result_has_filepath ({target.file_path}:{target.line_number})")


def test_recommendation_no_fake_module_paths():
    """Test that recommendations don't include fake module paths.

    Querying captureSnapshot should recommend webPageSnapshot in the same context,
    not fake paths like @ohos.web.webview.webview.webPageSnapshot.
    """
    from check_sdk_imports import query_mode

    # Uses _global_indexer rebuilt once at start
    results = query_mode("@ohos.web.webview.webview.WebviewController#captureSnapshot", _global_indexer)
    assert len(results) == 1, f"Expected 1 result, got {len(results)}"

    # Check recommendations
    recs = results[0].recommendations
    assert len(recs) > 0, "Should have recommendations"

    # First recommendation should be webPageSnapshot from the correct nested class path
    first_rec = recs[0].item
    assert "WebviewController" in first_rec, \
        f"First recommendation should contain WebviewController, got {first_rec}"
    assert "webPageSnapshot" in first_rec, \
        f"First recommendation should be webPageSnapshot, got {first_rec}"
    assert "WebviewController.WebviewController" not in first_rec, \
        f"Should not have doubled class name, got {first_rec}"

    print(f"PASS: test_recommendation_no_fake_module_paths ({len(recs)} recommendations)")


def test_interface_properties_not_extracted_as_members():
    """Test that interface properties inside braces are not extracted as namespace members.

    In @ohos.multimedia.audio, capturerInfo is a property of AudioCapturerOptions interface,
    not a standalone member of the audio namespace.
    """
    from check_sdk_imports import query_mode

    # Uses _global_indexer rebuilt once at start
    results = query_mode("@ohos.multimedia.audio", _global_indexer)
    assert len(results) > 0, "Should have results for audio module"

    # Get all member names from results (skip first which is the module itself)
    member_names = []
    for r in results[1:]:  # Skip first which is the module itself
        # Member format from query_mode: "  className (N members)"
        # The r.item is like "  audio (10 members)" or "  SomeClass (5 members)"
        stripped = r.item.strip()
        if stripped.startswith('('):
            continue
        # Parse "  Name (N members)" format
        parts = stripped.split(' (')
        if len(parts) >= 2:
            member_names.append(parts[0].strip())

    # capturerInfo should NOT be a member of audio namespace
    # (it's a property inside AudioCapturerOptions interface)
    assert "capturerInfo" not in member_names, \
        f"capturerInfo should not be a member of audio namespace, got members: {member_names}"

    # Similarly, capturerFlags is inside an interface
    assert "capturerFlags" not in member_names, \
        f"capturerFlags should not be a member of audio namespace, got members: {member_names}"

    print(f"PASS: test_interface_properties_not_extracted_as_members ({len(member_names)} members checked)")


def test_query_nonexistent_member_recommendation():
    """Test that querying non-existent member returns proper error path without duplication."""
    from check_sdk_imports import query_mode

    # Uses _global_indexer rebuilt once at start
    results = query_mode("@ohos.web.webview.webview.WebviewController#reload", _global_indexer)
    assert len(results) == 1, f"Expected 1 result, got {len(results)}"

    # Should NOT have duplicate WebviewController.WebviewController
    assert "WebviewController.WebviewController" not in results[0].item, \
        f"Error path should not duplicate class name: {results[0].item}"

    # Should be the correct path format
    assert results[0].item == "@ohos.web.webview.webview.WebviewController#reload", \
        f"Expected @ohos.web.webview.webview.WebviewController#reload, got {results[0].item}"
    assert results[0].status == Status.MEMBER_NOT_FOUND, \
        f"Expected MEMBER_NOT_FOUND status, got {results[0].status}"

    print(f"PASS: test_query_nonexistent_member_recommendation ({len(results[0].recommendations)} recommendations)")


def run_all_tests():
    """Run all tests."""
    global _global_indexer
    print("=" * 60)
    print("Running nested class indexing tests...")
    print("=" * 60)

    # Rebuild index once at the start to ensure consistent fresh data
    sdk_home = get_sdk_or_fail()
    _global_indexer = rebuild_index(sdk_home, ".sdk_index.json")

    test_nested_class_dataclass()
    test_parse_dts_file_returns_tuple()
    test_build_index_creates_synthetic_modules()
    test_query_nested_class_members()
    test_nested_class_has_correct_export_type()
    test_query_no_duplicates()
    test_query_nested_class_shows_members()
    test_partial_match_member_not_module()
    test_query_member_no_duplicate_path()
    test_query_nonexistent_member_recommendation()
    test_query_result_has_filepath()
    test_partial_query_result_has_filepath()
    test_recommendation_no_fake_module_paths()
    test_interface_properties_not_extracted_as_members()

    print("=" * 60)
    print("All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
