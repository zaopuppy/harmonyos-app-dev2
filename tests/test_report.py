import sys
import os

# Add harmony-api/scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'skills', 'harmony-api', 'scripts'))

from report import CheckResult, Status, format_console
from dataclasses import dataclass

@dataclass
class Recommendation:
    item: str
    member_name: str
    levenshtein_dist: int
    prefix_score: float
    combined_score: float
    source: str
    def sort_key(self): return -self.combined_score

results = [
    CheckResult('@ohos.app.ability.Ability', Status.OK),
    CheckResult('@ohos.app.ability.Ability#nonExistent', Status.MEMBER_NOT_FOUND,
        "member 'nonExistent' not found",
        recommendations=[
            Recommendation(
                '@ohos.app.ability.Ability#onConfigurationUpdate',
                'onConfigurationUpdate', 1, 0.0, 0.9, 'other_class'),
            Recommendation(
                '@ohos.app.ability.Ability#onWindowStageCreate',
                'onWindowStageCreate', 15, 0.5, 0.5, 'other_class'),
        ])
]
print(format_console(results))