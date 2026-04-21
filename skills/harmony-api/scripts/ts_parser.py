import re
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class ImportInfo:
    module: str          # '@ohos.app.ability.Ability'
    alias: str           # local binding 'Ability'
    is_default: bool     # True for default imports
    names: List[str]     # for {Foo, Bar} named imports


@dataclass
class MemberAccess:
    module: str           # '@ohos.app.ability.Ability'
    class_name: str       # 'Ability' (alias)
    member: str           # 'onConfigurationUpdate'
    line: int             # source line number


IMPORT_RE = re.compile(
    r'^import\s+(?:'
    r'(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]'   # import X from 'module'
    r'|'
    r'\{([^}]+)\}\s+from\s+[\'"]([^\'"]+)[\'"]'  # import { A, B } from 'module'
    r'|'
    r'\*\s+as\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]'  # import * as X from 'module'
    r'|'
    r'[\'"]([^\'"]+)[\'"]'                         # import 'module' (side-effect)
    r')',
    re.MULTILINE
)


def extract_imports(source: str) -> List[ImportInfo]:
    imports = []
    for m in IMPORT_RE.finditer(source):
        if m.group(1) is not None:
            # import X from 'module'
            imports.append(ImportInfo(
                module=m.group(2),
                alias=m.group(1),
                is_default=True,
                names=[]
            ))
        elif m.group(3) is not None:
            # import { A, B } from 'module'
            names = [n.strip() for n in m.group(3).split(',')]
            imports.append(ImportInfo(
                module=m.group(4),
                alias='',
                is_default=False,
                names=names
            ))
        elif m.group(5) is not None:
            # import * as X from 'module'
            imports.append(ImportInfo(
                module=m.group(6),
                alias=m.group(5),
                is_default=False,
                names=[]
            ))
        elif m.group(7) is not None:
            # import 'module' (side-effect)
            imports.append(ImportInfo(
                module=m.group(7),
                alias='',
                is_default=False,
                names=[]
            ))
    return imports


def detect_member_accesses(source: str, imports: List[ImportInfo]) -> List[MemberAccess]:
    accesses = []
    for imp in imports:
        # Determine the alias to look for
        if imp.is_default:
            alias = imp.alias
        elif imp.names:
            alias = imp.names[0]  # use first named import
        elif imp.alias:
            alias = imp.alias      # namespace import
        else:
            continue

        # Find alias.something patterns (method calls or property access)
        pattern = re.compile(rf'\b{re.escape(alias)}\.(\w+)(?=\s*[\(:.])')
        for m in pattern.finditer(source):
            member = m.group(1)
            line_num = source[:m.start()].count('\n') + 1
            accesses.append(MemberAccess(
                module=imp.module,
                class_name=alias,
                member=member,
                line=line_num
            ))
    return accesses


def parse_file(filepath: str) -> Tuple[List[ImportInfo], List[MemberAccess]]:
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    imports = extract_imports(source)
    # Strip line comments to avoid false matches
    source_stripped = re.sub(r'//.*$', '', source, flags=re.MULTILINE)
    accesses = detect_member_accesses(source_stripped, imports)
    return imports, accesses