"""Output report formatting for OpenHarmony SDK import checker."""
from dataclasses import dataclass
from enum import Enum
from typing import List


class Status(Enum):
    OK = "✓"
    MODULE_NOT_FOUND = "✗"
    CLASS_NOT_FOUND = "✗"
    MEMBER_NOT_FOUND = "✗"


@dataclass
class CheckResult:
    item: str       # e.g. "@ohos.app.ability.Ability.Ability#onConfigurationUpdate"
    status: Status
    detail: str = ""
    recommendations: list = None  # List[Recommendation] - filled from recommender
    file_path: str = ""   # Path to the .d.ts file where this item is defined
    line_number: int = 0  # Line number in the .d.ts file where this item is defined

    def __post_init__(self):
        if self.recommendations is None:
            self.recommendations = []


def format_console(results: List[CheckResult]) -> str:
    """Format results for console output."""
    lines = []
    passed = sum(1 for r in results if r.status == Status.OK)
    failed = len(results) - passed

    for r in results:
        icon = r.status.value
        detail = f" ({r.detail})" if r.detail else ""
        # Normalize path separators and show line number
        file_info = ""
        if r.file_path:
            normalized = r.file_path.replace('\\', '/')
            if r.line_number > 0:
                file_info = f" [{normalized}:{r.line_number}]"
            else:
                file_info = f" [{normalized}]"
        lines.append(f"[{icon}] {r.item}{detail}{file_info}")

        # Print recommendations for failed items
        if r.status != Status.OK and r.recommendations:
            lines.append("    Did you mean:")
            for rec in r.recommendations:
                reason = (f"Levenshtein dist={rec.levenshtein_dist}"
                          if rec.levenshtein_dist > 0
                          else f"prefix_score={rec.prefix_score:.2f}")
                lines.append(f"      → {rec.item} ({reason})")

    lines.append(f"\nSummary: {passed} passed, {failed} failed")
    return "\n".join(lines)


def format_json(results: List[CheckResult]) -> str:
    """Format results as JSON."""
    import json
    return json.dumps(
        [
            {
                "item": r.item,
                "status": r.status.name,
                "detail": r.detail,
                "file_path": r.file_path.replace('\\', '/') if r.file_path else "",
                "line_number": r.line_number,
                "recommendations": [
                    {
                        "item": rec.item,
                        "levenshtein_dist": rec.levenshtein_dist,
                        "prefix_score": rec.prefix_score
                    }
                    for rec in (r.recommendations or [])
                ]
            }
            for r in results
        ],
        indent=2,
        ensure_ascii=False
    )
