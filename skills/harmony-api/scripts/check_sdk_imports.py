#!/usr/bin/env python3
"""
OpenHarmony SDK Import & API Checker
Checks whether imports and API calls in .ts/.ets files exist in the SDK.
"""
import argparse
import os
import sys
from pathlib import Path
from typing import List

# Import our modules
from sdk_indexer import SDKIndexer
from ts_parser import parse_file, ImportInfo, MemberAccess
from report import Status, CheckResult, format_console, format_json
from recommender import recommend, recommend_module


def parse_args():
    parser = argparse.ArgumentParser(
        description="Check OpenHarmony SDK imports and API availability"
    )
    parser.add_argument(
        "--path",
        default=None,
        help="Project path or .ts/.ets file to scan"
    )
    parser.add_argument(
        "--sdk-home",
        default=os.environ.get("DEVECO_SDK_HOME"),
        help="Override DEVECO_SDK_HOME environment variable"
    )
    parser.add_argument(
        "--rebuild-index",
        action="store_true",
        help="Force rebuild SDK index"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show verbose progress messages"
    )
    parser.add_argument(
        "--query",
        default=None,
        help="Query mode: @ohos.module, @ohos.module.ClassName, or @ohos.module.ClassName#member"
    )
    parser.add_argument(
        "--no-recommend",
        action="store_true",
        help="Disable recommendations on failure"
    )
    return parser.parse_args()


def find_hdc() -> str:
    """
    Search for hdc binary in PATH or common SDK toolchains locations.
    Returns the full path to hdc/hdc.exe if found, else None.
    """
    # Try PATH first
    for name in ('hdc', 'hdc.exe'):
        for dir_path in os.environ.get('PATH', '').split(os.pathsep):
            candidate = os.path.join(dir_path, name)
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate
            # On Windows, also check without X_OK
            if os.name == 'nt' and os.path.isfile(candidate):
                return candidate

    # Try common SDK toolchains locations under DEVECO_SDK_HOME
    sdk_home = os.environ.get('DEVECO_SDK_HOME', '')
    if sdk_home:
        for suffix in ('openharmony/toolchains/hdc', 'openharmony/toolchains/hdc.exe',
                       'HMS/toolchains/hdc', 'HMS/toolchains/hdc.exe'):
            candidate = os.path.join(sdk_home, 'default', suffix)
            if os.path.isfile(candidate):
                return candidate

    return None


def derive_sdk_home_from_hdc(hdc_path: str) -> str:
    """
    Derive DEVECO_SDK_HOME from an hdc binary path.
    hdc is always at {DEVECO_SDK_HOME}/default/openharmony/toolchains/hdc[.exe],
    so strip '/default/openharmony/toolchains/hdc[.exe]' to recover DEVECO_SDK_HOME.

    Example:
        C:/Program Files/Huawei/DevEco Studio/sdk/default/openharmony/toolchains/hdc.exe
        → C:/Program Files/Huawei/DevEco Studio/sdk
    """
    normalized = hdc_path.replace('\\', '/')

    for suffix in ('/default/openharmony/toolchains/hdc.exe', '/default/openharmony/toolchains/hdc'):
        if normalized.endswith(suffix):
            return normalized[:-len(suffix)]

    raise ValueError(f"Cannot derive SDK_HOME from hdc path: {hdc_path}")


def find_sdk_home() -> str:
    """
    Find DEVECO_SDK_HOME from environment or hdc path.
    Returns the SDK path or None if not found.
    """
    sdk_home = os.environ.get('DEVECO_SDK_HOME')
    if sdk_home:
        return sdk_home

    hdc_path = find_hdc()
    if hdc_path:
        return derive_sdk_home_from_hdc(hdc_path)

    return None


# SDK module prefixes that we check
SDK_MODULE_PREFIXES = ('@ohos', '@kit', '@system', '@hms', '@native', '@ark')


def is_sdk_module(module: str) -> bool:
    """Check if a module belongs to the SDK (not third-party)."""
    return any(module.startswith(p) for p in SDK_MODULE_PREFIXES)


def check_import(imp: ImportInfo, indexer: SDKIndexer, recommend_enabled: bool = True) -> CheckResult:
    """Check if an import module exists in SDK. Skip non-SDK modules."""
    item = imp.module

    # Skip third-party modules not in SDK
    if not is_sdk_module(imp.module):
        return CheckResult(item, Status.OK)

    mod = indexer.get(imp.module)
    if not mod:
        # Module not found — recommend similar module names
        recs = []
        if recommend_enabled:
            recs = recommend_module(imp.module, indexer, top_n=3)
        return CheckResult(item, Status.MODULE_NOT_FOUND, "module not found", recommendations=recs)
    return CheckResult(item, Status.OK)


def check_member_access(acc: MemberAccess, indexer: SDKIndexer, recommend_enabled: bool = True, context_module: str = None) -> CheckResult:
    """Check if a member access (class#member) exists in SDK. Skip non-SDK modules."""
    item = f"{acc.module}.{acc.class_name}#{acc.member}"

    # Skip third-party modules not in SDK
    if not is_sdk_module(acc.module):
        return CheckResult(item, Status.OK)

    mod = indexer.get(acc.module)
    if not mod:
        recs = recommend(acc.member, indexer, top_n=3, context_module=context_module) if recommend_enabled else []
        return CheckResult(item, Status.MODULE_NOT_FOUND, "module not found", recommendations=recs)

    # Find the class
    cls = None
    for cname, cinfo in mod.classes.items():
        if cname == acc.class_name:
            cls = cinfo
            break

    if not cls:
        # Try treating class_name as a submodule path (e.g., webview in @kit.ArkWeb might be @kit.ArkWeb.webview)
        submodule_name = f"{acc.module}.{acc.class_name}"
        submod = indexer.get(submodule_name)
        if submod:
            # Check if member exists in any class of the submodule
            for sub_cname, sub_cinfo in submod.classes.items():
                if acc.member in sub_cinfo.members or acc.member in sub_cinfo.statics:
                    return CheckResult(item, Status.OK)
        recs = recommend(acc.member, indexer, top_n=3, context_module=context_module) if recommend_enabled else []
        return CheckResult(item, Status.CLASS_NOT_FOUND, f"class '{acc.class_name}' not found", recommendations=recs)

    if acc.member not in cls.members and acc.member not in cls.statics:
        recs = recommend(acc.member, indexer, top_n=3, context_module=context_module) if recommend_enabled else []
        return CheckResult(item, Status.MEMBER_NOT_FOUND, f"member '{acc.member}' not found in class '{acc.class_name}'", recommendations=recs)

    return CheckResult(item, Status.OK)


class TSScanner:
    """Scans a directory (or single file) for .ts/.ets files and extracts imports/member accesses."""

    def __init__(self, path: str, verbose: bool = False):
        self.path = path
        self.verbose = verbose

    def scan(self) -> tuple[List[ImportInfo], List[MemberAccess]]:
        """Scan all .ts/.ets files (or single file) in the path, return all imports and member accesses."""
        all_imports = []
        all_accesses = []

        if os.path.isfile(self.path):
            # Single file mode
            if self.path.endswith(('.ts', '.ets')):
                try:
                    imports, accesses = parse_file(self.path)
                    all_imports.extend(imports)
                    all_accesses.extend(accesses)
                except Exception as e:
                    if self.verbose:
                        print(f"Warning: failed to parse {self.path}: {e}")
            return all_imports, all_accesses

        # Directory mode
        for root, _, files in os.walk(self.path):
            # Skip common non-source directories
            skip_dirs = {'.git', 'node_modules', '.sdk_index.json', 'build', 'dist'}
            if any(d in root for d in skip_dirs):
                continue

            for fname in files:
                if fname.endswith(('.ts', '.ets')):
                    fpath = os.path.join(root, fname)
                    try:
                        imports, accesses = parse_file(fpath)
                        all_imports.extend(imports)
                        all_accesses.extend(accesses)
                    except Exception as e:
                        if self.verbose:
                            print(f"Warning: failed to parse {fpath}: {e}")
                        continue

        return all_imports, all_accesses


def query_mode(query_str: str, indexer: SDKIndexer) -> List[CheckResult]:
    """
    Handle --query mode.
    Formats:
      @ohos.XXX           → list all classes in module
      @ohos.XXX.ClassName → list all members in class
      @ohos.XXX.ClassName#member → check member, recommend if not found
    """
    if '#' in query_str:
        # Query member: @ohos.module.ClassName#member
        # Module may contain dots, so find it by checking which prefix exists in index
        class_and_member = query_str.rsplit('#', 1)[0]  # e.g. "@ohos.app.ability.Ability.Ability"
        member_name = query_str.rsplit('#', 1)[1]        # e.g. "onConfigurationUpdate"

        # First, try direct module lookup (entire string before # as module name)
        mod = indexer.get(class_and_member)

        module_name = class_and_member
        class_name = None

        if mod:
            # Direct module found - use its first (and usually only) class
            if mod.classes:
                class_name = list(mod.classes.keys())[0]
                # Check if this is a synthetic nested class module
                # (5+ parts where last part = class name, and class_name == last segment)
                parts = module_name.split('.')
                if len(parts) > 4 and class_name == parts[-1]:
                    # Synthetic nested class - class_name is already included in module path
                    # Use module_name directly without appending class_name
                    full = f"{module_name}#{member_name}"
                else:
                    full = f"{module_name}.{class_name}#{member_name}"
        else:
            # Fallback: find module by testing which prefix exists in index
            module_name = None
            parts = class_and_member.split('.')
            for i in range(1, len(parts) + 1):
                candidate_module = '.'.join(parts[:i])
                candidate_class = '.'.join(parts[i:])
                if indexer.get(candidate_module):
                    module_name = candidate_module
                    class_name = candidate_class
                    # Don't break - continue to find the longest valid module prefix

            if not module_name:
                # Fallback: treat all but last part as module, last as class
                module_name = '.'.join(parts[:-1])
                class_name = parts[-1]

            mod = indexer.get(module_name)
            full = f"{module_name}.{class_name}#{member_name}" if class_name else f"{module_name}#{member_name}"

        mod = indexer.get(module_name)
        if not mod:
            recs = recommend(member_name, indexer, top_n=3)
            return [CheckResult(full, Status.MODULE_NOT_FOUND, "module not found", recommendations=recs)]

        cls = mod.classes.get(class_name) if class_name else None
        if not cls:
            recs = recommend(member_name, indexer, top_n=3)
            return [CheckResult(full, Status.CLASS_NOT_FOUND, f"class '{class_name}' not found", recommendations=recs, file_path=mod.file, line_number=0)]

        if member_name not in cls.members and member_name not in cls.statics:
            recs = recommend(member_name, indexer, top_n=3)
            return [CheckResult(full, Status.MEMBER_NOT_FOUND, f"member '{member_name}' not found", recommendations=recs, file_path=mod.file, line_number=cls.line_number)]

        return [CheckResult(full, Status.OK, file_path=mod.file, line_number=cls.line_number)]

    elif query_str.startswith('@ohos.') or query_str.startswith('@hms.'):
        # Query module or module.class
        # First try direct module lookup
        show_members_directly = False  # Flag for synthetic nested class case
        mod = indexer.get(query_str)
        if mod:
            module_name = query_str
            class_name = None
            # If module has exactly one class with same name as last path component,
            # AND query has 3+ dot segments (likely a nested class path),
            # show its members directly (synthetic nested class case)
            if len(mod.classes) == 1 and query_str.count('.') >= 3:
                cls_name = list(mod.classes.keys())[0]
                if query_str.endswith(cls_name):
                    class_name = cls_name
                    show_members_directly = True
        else:
            # Find module by testing which prefix exists in index
            parts = query_str.split('.')
            module_name = None
            class_name = None

            for i in range(1, len(parts) + 1):
                candidate_module = '.'.join(parts[:i])
                candidate_class = '.'.join(parts[i:])
                if indexer.get(candidate_module):
                    module_name = candidate_module
                    class_name = candidate_class
                    # Don't break - continue to find the longest valid module prefix

            if not module_name:
                # No valid module found
                mod_part = query_str.rsplit('.', 1)[-1]
                recs = recommend(mod_part, indexer, top_n=3)
                return [CheckResult(query_str, Status.MODULE_NOT_FOUND, "module not found", recommendations=recs)]

            mod = indexer.get(module_name)

        if not class_name:
            # Query module: list all classes
            results = [CheckResult(query_str, Status.OK, file_path=mod.file)]
            for class_name, class_info in mod.classes.items():
                members = class_info.members + class_info.statics
                results.append(CheckResult(f"  {class_name} ({len(members)} members)", Status.OK, file_path=mod.file, line_number=class_info.line_number))
            return results

        # Query module.class: list all members
        cls = mod.classes.get(class_name) if class_name else None
        if not cls:
            recs = recommend(class_name, indexer, top_n=3)
            return [CheckResult(f"{module_name}.{class_name}", Status.CLASS_NOT_FOUND, f"class '{class_name}' not found", recommendations=recs, file_path=mod.file, line_number=0)]

        # Use query_str for display when showing synthetic nested class members
        display_path = query_str if show_members_directly else f"{module_name}.{class_name}"
        results = [CheckResult(display_path, Status.OK, file_path=mod.file, line_number=cls.line_number)]
        for member in cls.members + cls.statics:
            results.append(CheckResult(f"  {member}", Status.OK))
        return results

    else:
        # Partial match - search modules AND members
        # Only match query against the LAST segment of module path (not arbitrary substrings)
        # Exclude synthetic nested class modules and modules that don't make sense as standalone APIs
        all_modules = indexer.get_module_list()
        module_matches = []
        for m in all_modules:
            # Synthetic nested class modules: @ohos.X.Y.Z.Z (5+ parts, class Z in module Z)
            parts = m.split('.')
            if len(parts) > 4 and parts[-1] == parts[-2]:
                continue
            if m.rsplit('.', 1)[-1] == query_str:
                module_matches.append(m)

        # Also search member names across all modules
        member_results = []
        for mod_name, mod_info in indexer.modules.items():
            # Skip synthetic nested class modules for member search
            parts = mod_name.split('.')
            # Synthetic nested class module: @ohos.X.Y.Z.Z (5+ parts, class Z in module Z)
            if len(parts) > 4 and parts[-1] == parts[-2]:
                continue
            for class_name, class_info in mod_info.classes.items():
                for member in class_info.members + class_info.statics:
                    if query_str in member:
                        # For nested class modules where class_name == last segment of mod_name,
                        # construct path as mod_name#member to avoid doubled class name
                        if class_name == mod_name.rsplit('.', 1)[-1]:
                            path = f"{mod_name}#{member}"
                        else:
                            path = f"{mod_name}.{class_name}.{member}"
                        if path == query_str:
                            continue
                        # Skip when class_name equals the last segment of mod_name
                        # This creates a path that looks like a module hierarchy
                        # e.g., @ohos.web.webview + webview class = @ohos.web.webview.webview.webPageSnapshot
                        # which looks like module @ohos.web.webview.webview + member webPageSnapshot
                        if class_name == mod_name.rsplit('.', 1)[-1]:
                            # For nested class modules (class_name == last segment of mod_name),
                            # use mod_name to check if the module exists - this is a valid nested class path
                            if not indexer.get(mod_name):
                                continue
                        member_results.append(CheckResult(
                            path,
                            Status.OK,
                            file_path=mod_info.file,
                            line_number=class_info.line_number
                        ))

        if not module_matches and not member_results:
            return [CheckResult(query_str, Status.MODULE_NOT_FOUND, "no matching modules or members found")]

        # Deduplicate while preserving order (same path can appear in both lists)
        seen = set()
        unique_results = []
        for m in module_matches[:10]:
            if m not in seen:
                seen.add(m)
                mod_info = indexer.get(m)
                unique_results.append(CheckResult(m, Status.OK, file_path=mod_info.file if mod_info else ""))
        for result in member_results[:10]:
            if result.item not in seen:
                seen.add(result.item)
                unique_results.append(result)

        return unique_results


def main():
    args = parse_args()

    # Must specify either --path or --query
    if not args.query and not args.path:
        print("Error: must specify either --path or --query")
        return 1

    if args.query and args.path:
        print("Error: --query and --path are mutually exclusive")
        return 1

    sdk_home = args.sdk_home
    if not sdk_home:
        # Auto-detect hdc from PATH or common locations to derive SDK_HOME
        hdc_path = find_hdc()
        if hdc_path:
            try:
                sdk_home = derive_sdk_home_from_hdc(hdc_path)
            except ValueError as e:
                print(f"Error: {e}")
                return 1
        else:
            print("Error: DEVECO_SDK_HOME not set and hdc not found in PATH")
            return 1

    recommend_enabled = not args.no_recommend

    # Index path: always use script's own directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(script_dir, ".sdk_index.json")

    # Load or build index
    indexer = SDKIndexer(sdk_home, index_path)

    if args.rebuild_index or indexer.needs_rebuild():
        if args.verbose:
            print("Building SDK index...")
        indexer.build_index()
        indexer.save()
        if args.verbose:
            print(f"Index saved to {index_path}")
    else:
        indexer.load()
        if args.verbose:
            print(f"Loaded index from {index_path}")

    if args.verbose:
        print(f"Indexed {len(indexer.modules)} modules")

    # Query mode
    if args.query:
        if args.verbose:
            print(f"Query mode: {args.query}")
        results = query_mode(args.query, indexer)
        output = format_json(results) if args.json else format_console(results)
        print(output)
        return 1 if any(r.status != Status.OK for r in results) else 0

    # File/directory scan mode
    if args.verbose:
        print(f"Scanning {args.path} for .ts/.ets files...")

    scanner = TSScanner(args.path, verbose=args.verbose)
    all_imports, all_accesses = scanner.scan()

    if args.verbose:
        print(f"Found {len(all_imports)} imports, {len(all_accesses)} member accesses")

    # Check everything
    results = []
    for imp in all_imports:
        results.append(check_import(imp, indexer, recommend_enabled))

    for acc in all_accesses:
        results.append(check_member_access(acc, indexer, recommend_enabled, context_module=acc.module))

    # Output
    if args.json:
        print(format_json(results))
    else:
        print("=== OpenHarmony SDK Import & API Check ===")
        print(f"SDK: {sdk_home}")
        print(f"Path: {args.path}")
        print(f"Imports checked: {len(all_imports)}, Member accesses: {len(all_accesses)}")
        print()
        print(format_console(results))

    # Return exit code
    has_failures = any(r.status != Status.OK for r in results)
    return 1 if has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
