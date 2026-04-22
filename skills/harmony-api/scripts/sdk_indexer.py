"""
SDK Indexer for OpenHarmony SDK.
Builds and caches an index of .d.ts files with their class and member information.
"""

import os
import re
import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, Optional, List, Iterator, Tuple


SDK_SUBDIRS = [
    "default/openharmony/ets/api",
    "default/openharmony/ets/arkts",
    "default/openharmony/ets/component",
    "default/openharmony/ets/kits",
    "default/hms/etc/api",
    "default/hms/etc/kits",
]


@dataclass
class ClassInfo:
    members: list      # 方法名 + 属性名列表
    statics: list       # 静态成员列表
    export_type: str    # "default" 或 "named"
    line_number: int = 0  # Line number where this class is defined


@dataclass
class NestedClass:
    parent_module: str      # '@ohos.web.webview'
    namespace: str         # 'webview'
    class_name: str        # 'WebviewController'
    members: list
    statics: list
    line_number: int = 0   # Line number where nested class is defined


@dataclass
class ModuleInfo:
    file: str           # .d.ts 文件完整路径
    classes: Dict[str, ClassInfo]  # 类名 -> ClassInfo


class SDKIndexer:
    def __init__(self, sdk_home: str, index_path: str):
        self.sdk_home = sdk_home
        self.index_path = index_path
        self.modules: Dict[str, ModuleInfo] = {}  # key = module name like "@ohos.app.ability.Ability"

    def _dts_files_in_subdir(self, subdir: str):
        """Yield all .d.ts file paths in a subdirectory (recursive)."""
        full_dir = os.path.join(self.sdk_home, subdir)
        if not os.path.isdir(full_dir):
            return
        for root, _, files in os.walk(full_dir):
            for fname in files:
                if fname.endswith('.d.ts'):
                    yield os.path.join(root, fname)

    def get_sdk_mtime(self) -> float:
        """Walk all SDK subdirs, return latest .d.ts file mtime."""
        latest_mtime = 0.0
        for subdir in SDK_SUBDIRS:
            for filepath in self._dts_files_in_subdir(subdir):
                try:
                    mtime = os.path.getmtime(filepath)
                    if mtime > latest_mtime:
                        latest_mtime = mtime
                except OSError:
                    continue
        return latest_mtime

    def needs_rebuild(self) -> bool:
        """True if index_path doesn't exist OR sdk has newer files."""
        if not os.path.exists(self.index_path):
            return True
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            cached_mtime = data.get('sdk_mtime', 0)
            return self.get_sdk_mtime() > cached_mtime
        except (json.JSONDecodeError, IOError):
            return True

    def _strip_comments_and_strings(self, content: str) -> str:
        """Remove single-line and multi-line comments and string literals from d.ts content."""
        # Remove multi-line comments /* ... */
        content = re.sub(r'/\*[\s\S]*?\*/', '', content)
        # Remove single-line comments //
        content = re.sub(r'//.*', '', content)
        # Remove string literals (single and double quoted, template literals)
        content = re.sub(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|`(?:[^`\\]|\\.)*`', '', content)
        return content

    @staticmethod
    def _get_module_name_from_filepath(filepath: str) -> str:
        """Get module name from filepath, properly handling .d.ts extension."""
        basename = os.path.basename(filepath)
        # Handle .d.ts extension properly (not just .ts)
        if basename.endswith('.d.ts'):
            return basename[:-5]  # Remove '.d.ts'
        return os.path.splitext(basename)[0]

    def _parse_dts_file(self, filepath: str) -> Tuple[Optional[ModuleInfo], List[NestedClass]]:
        """Parse one .d.ts file and return ModuleInfo or None."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except (IOError, UnicodeDecodeError):
            return None, []

        # Module name = basename without extension
        module_name = self._get_module_name_from_filepath(filepath)

        # Strip comments and strings for safer regex matching
        clean_content = self._strip_comments_and_strings(content)

        classes = {}
        nested_classes = []

        # Find class bodies - we need to find the { and matching } for each class
        def extract_body(content: str, start_pos: int) -> tuple:
            """Extract body from opening { to matching }. Returns (body, end_pos)."""
            depth = 0
            body_start = content.find('{', start_pos)
            if body_start == -1:
                return None, None
            pos = body_start
            while pos < len(content):
                c = content[pos]
                if c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        return content[body_start + 1:pos], pos + 1
                pos += 1
            return None, None

        def extract_members(body: str) -> list:
            """Extract member names from a class or namespace body."""
            members = []
            paren_depth = 0
            brace_depth = 0
            current = []
            for char in body:
                if char == '(':
                    paren_depth += 1
                    current.append(char)
                elif char == ')':
                    paren_depth -= 1
                    current.append(char)
                elif char == '{':
                    brace_depth += 1
                    current.append(char)
                elif char == '}':
                    brace_depth -= 1
                    current.append(char)
                elif char == ';' and paren_depth == 0 and brace_depth == 0:
                    decl = ''.join(current).strip()
                    current = []
                    if not decl:
                        continue

                    if decl.startswith('constructor'):
                        if 'constructor' not in members:
                            members.append('constructor')
                        continue

                    paren_idx = decl.find('(')
                    if paren_idx != -1:
                        before_paren = decl[:paren_idx].strip()
                        words = before_paren.split()
                        if words:
                            name = words[-1]
                            if name and name not in (
                                'if', 'else', 'for', 'while', 'do',
                                'switch', 'try', 'catch', 'finally',
                                'get', 'set'):
                                if name not in members:
                                    members.append(name)
                    else:
                        colon_idx = decl.find(':')
                        if colon_idx != -1:
                            name = decl[:colon_idx].strip().split()[-1]
                            if name and name not in (
                                'if', 'else', 'for', 'while', 'do',
                                'switch', 'try', 'catch', 'finally',
                                'type'):
                                if name not in members:
                                    members.append(name)
                else:
                    current.append(char)
            return members

        def pos_to_line(content: str, pos: int) -> int:
            """Convert byte/char position to line number (1-based)."""
            return content[:pos].count('\n') + 1

        # Process: export default class Foo { }
        for match in re.finditer(r'export\s+default\s+class\s+(\w+)\s*\{', clean_content):
            class_name = match.group(1)
            body, _ = extract_body(clean_content, match.end() - 1)
            if body is not None:
                classes[class_name] = ClassInfo(
                    members=extract_members(body),
                    statics=[],
                    export_type="default",
                    line_number=pos_to_line(content, match.start())
                )

        # Process: export class Foo { }
        for match in re.finditer(r'export\s+class\s+(\w+)\s*\{', clean_content):
            class_name = match.group(1)
            if class_name in classes:
                continue
            body, _ = extract_body(clean_content, match.end() - 1)
            if body is not None:
                classes[class_name] = ClassInfo(
                    members=extract_members(body),
                    statics=[],
                    export_type="named",
                    line_number=pos_to_line(content, match.start())
                )

        # Process: export namespace Foo { }, declare namespace Foo { }, or namespace Foo { }
        # These are treated as "classes" for API matching purposes
        for match in re.finditer(r'(?:(?:export|declare)\s+)?namespace\s+(\w+)\s*\{', clean_content):
            ns_name = match.group(1)
            body, _ = extract_body(clean_content, match.end() - 1)
            if body is not None:
                ns_members = extract_members(body)
                # Also extract nested class names from the namespace body
                for class_match in re.finditer(r'(?:export\s+)?class\s+(\w+)\s*\{', body):
                    nested_class_name = class_match.group(1)
                    if nested_class_name not in ns_members:
                        ns_members.append(nested_class_name)
                    # Extract nested class body and members
                    class_body_start = class_match.end() - 1
                    class_body, _ = extract_body(body, class_body_start)
                    if class_body is not None:
                        nested_members = extract_members(class_body)
                        # Find line number in original content by searching for the class declaration
                        class_search = f'class {nested_class_name}'
                        class_pos_in_original = content.find(class_search)
                        nested_line = (content[:class_pos_in_original].count('\n') + 1
                                      if class_pos_in_original >= 0 else 0)
                        nested_classes.append(NestedClass(
                            parent_module=self._get_module_name_from_filepath(filepath),
                            namespace=ns_name,
                            class_name=nested_class_name,
                            members=nested_members,
                            statics=[],
                            line_number=nested_line
                        ))
                if ns_members:
                    # Find line number in original content by searching for the namespace declaration
                    ns_search = f'namespace {ns_name}'
                    ns_pos_in_original = content.find(ns_search)
                    ns_line = content[:ns_pos_in_original].count('\n') + 1 if ns_pos_in_original >= 0 else 0
                    classes[ns_name] = ClassInfo(
                        members=ns_members,
                        statics=[],
                        export_type="namespace",
                        line_number=ns_line
                    )

        # Process: declare [abstract] class Foo { } + separate export default Foo;
        # This covers the common HarmonyOS pattern where declaration and export are on separate lines.
        for match in re.finditer(r'\bdeclare\s+(?:abstract\s+)?class\s+(\w+)\b', clean_content):
            class_name = match.group(1)
            if class_name in classes:
                continue
            if not re.search(rf'\bexport\s+default\s+{re.escape(class_name)}\s*;', clean_content):
                continue
            body, _ = extract_body(clean_content, match.end())
            if body is not None:
                classes[class_name] = ClassInfo(
                    members=extract_members(body),
                    statics=[],
                    export_type="default",
                    line_number=pos_to_line(content, match.start())
                )

        # If no classes/namespaces found, check if this is a barrel file (re-export module)
        if not classes:
            return None, []

        return ModuleInfo(
            file=filepath,
            classes=classes
        ), nested_classes

    def _resolve_barrel_reexports(self, mod_info: ModuleInfo, mod_name: str) -> None:
        """
        For @kit barrel files with no class definitions, parse the file to find
        re-exports from other modules and create virtual class entries.
        e.g. @kit.CoreFileKit imports statfs from @ohos.file.statvfs,
        so we create class 'statfs' in @kit.CoreFileKit with the same members as @ohos.file.statvfs.statfs.
        """
        try:
            with open(mod_info.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except (IOError, UnicodeDecodeError):
            return

        # Find all import ... from '...' statements (both default and named)
        # Pattern: import X from 'module' or import { X } from 'module' or import X, { Y } from 'module'
        import_pattern = re.compile(
            r'import\s+(?:'
            r'(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]'   # default import: import statfs from '...'
            r'|'
            r'\{([^}]+)\}\s+from\s+[\'"]([^\'"]+)[\'"]'  # named import: import { statfs } from '...'
            r'|'
            r'(\w+)\s*,\s*\{([^}]+)\}\s+from\s+[\'"]([^\'"]+)[\'"]'  # mixed: import fs, { stat } from '...'
            r')',
            re.MULTILINE
        )

        resolved_classes = {}

        for match in import_pattern.finditer(content):
            if match.group(1) and match.group(2):
                # Default import: import statfs from '@ohos.file.statvfs'
                local_name = match.group(1)
                ref_module = match.group(2)
                self._copy_class_from_reexport(resolved_classes, local_name, ref_module, local_name)
            elif match.group(3) and match.group(4):
                # Named import: import { statfs } from '@ohos.file.statvfs'
                names = [n.strip() for n in match.group(3).split(',')]
                ref_module = match.group(4)
                for name in names:
                    self._copy_class_from_reexport(resolved_classes, name, ref_module, name)
            elif match.group(5) and match.group(6) and match.group(7):
                # Mixed: import fs, { stat } from '...'
                local_default = match.group(5)
                ref_module = match.group(7)
                # The named imports are in group(6)
                names = [n.strip() for n in match.group(6).split(',')]
                # local_default is the default import, not a re-export of a named item
                for name in names:
                    self._copy_class_from_reexport(resolved_classes, name, ref_module, name)

        mod_info.classes = resolved_classes

    def _copy_class_from_reexport(self, resolved_classes: dict,
                                  local_name: str, ref_module: str,
                                  ref_class_name: str) -> None:
        """Look up ref_module and copy ref_class_name's members into resolved_classes[local_name]."""
        ref_mod_info = self.modules.get(ref_module)
        if not ref_mod_info:
            return

        # Look for the class in the referenced module
        ref_class = ref_mod_info.classes.get(ref_class_name)
        if not ref_class:
            # Try case-insensitive match (some modules may differ in naming)
            for cname, cinfo in ref_mod_info.classes.items():
                if cname.lower() == ref_class_name.lower():
                    ref_class = cinfo
                    break

        if ref_class:
            resolved_classes[local_name] = ClassInfo(
                members=list(ref_class.members),
                statics=list(ref_class.statics),
                export_type=f"reexport:{ref_module}.{ref_class_name}"
            )

    def build_index(self) -> None:
        """Walk all SDK subdirs, call _parse_dts_file on each .d.ts, populate self.modules."""
        self.modules = {}
        all_nested_classes = []  # Collect all nested classes

        for subdir in SDK_SUBDIRS:
            for filepath in self._dts_files_in_subdir(subdir):
                module_info, nested_classes = self._parse_dts_file(filepath)

                module_name = self._get_module_name_from_filepath(filepath)
                if module_info:
                    self.modules[module_name] = module_info
                    all_nested_classes.extend(nested_classes)
                elif module_name.startswith('@kit.') and not module_info:
                    # Barrel file with no class definitions - add placeholder for second-pass resolution
                    self.modules[module_name] = ModuleInfo(file=filepath, classes={})

        # Second pass: resolve @kit barrel re-exports
        for mod_name, mod_info in self.modules.items():
            if mod_name.startswith('@kit.') and not mod_info.classes:
                self._resolve_barrel_reexports(mod_info, mod_name)

        # Third pass: create synthetic modules for nested classes
        for nc in all_nested_classes:
            synthetic_module_name = f"{nc.parent_module}.{nc.namespace}.{nc.class_name}"
            parent_file = self.modules[nc.parent_module].file if nc.parent_module in self.modules else ""
            self.modules[synthetic_module_name] = ModuleInfo(
                file=parent_file,
                classes={nc.class_name: ClassInfo(
                    members=nc.members,
                    statics=nc.statics,
                    export_type="nested",
                    line_number=nc.line_number
                )}
            )

    def save(self) -> None:
        """Write self.modules to self.index_path as JSON."""
        sdk_mtime = self.get_sdk_mtime()

        modules_json = {}
        for name, mod_info in self.modules.items():
            classes_json = {}
            for class_name, class_info in mod_info.classes.items():
                classes_json[class_name] = {
                    "members": class_info.members,
                    "statics": class_info.statics,
                    "export_type": class_info.export_type,
                    "line_number": class_info.line_number
                }
            modules_json[name] = {
                "file": mod_info.file,
                "classes": classes_json
            }

        data = {
            "version": 2,
            "built_at": time.time(),
            "sdk_mtime": sdk_mtime,
            "modules": modules_json
        }

        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self) -> None:
        """Load JSON from self.index_path and reconstruct self.modules."""
        self.modules = {}
        with open(self.index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        modules_data = data.get('modules', {})
        for module_name, module_data in modules_data.items():
            classes = {}
            for class_name, class_data in module_data.get('classes', {}).items():
                classes[class_name] = ClassInfo(
                    members=class_data.get('members', []),
                    statics=class_data.get('statics', []),
                    export_type=class_data.get('export_type', 'named'),
                    line_number=class_data.get('line_number', 0)
                )
            self.modules[module_name] = ModuleInfo(
                file=module_data.get('file', ''),
                classes=classes
            )

    def get(self, module_name: str) -> Optional[ModuleInfo]:
        """Get ModuleInfo by module name."""
        return self.modules.get(module_name)

    def has_member(self, module_name: str, class_name: str, member_name: str) -> bool:
        """Check if member exists in class."""
        mod = self.modules.get(module_name)
        if not mod:
            return False
        class_info = mod.classes.get(class_name)
        if not class_info:
            return False
        return member_name in class_info.members or member_name in class_info.statics

    def iter_all_members(self) -> Iterator[Tuple[str, str, str]]:
        """
        Iterate all (module_name, class_name, member_name) tuples.
        Yields every member from every class in every module.
        """
        for mod_name, mod_info in self.modules.items():
            for class_name, class_info in mod_info.classes.items():
                for mbr in class_info.members + class_info.statics:
                    yield mod_name, class_name, mbr

    def get_module_list(self) -> List[str]:
        """Return list of all module names."""
        return list(self.modules.keys())

    def get_class_list(self, module_name: str) -> Optional[List[str]]:
        """Return list of class names in a module, or None if module not found."""
        mod = self.modules.get(module_name)
        if not mod:
            return None
        return list(mod.classes.keys())

    def get_member_list(self, module_name: str, class_name: str) -> Optional[List[str]]:
        """Return list of members in a class, or None if module or class not found."""
        mod = self.modules.get(module_name)
        if not mod:
            return None
        class_info = mod.classes.get(class_name)
        if not class_info:
            return None
        return class_info.members + class_info.statics


