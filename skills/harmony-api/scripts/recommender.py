"""
Recommender for SDK members based on edit distance and prefix matching.
"""

from dataclasses import dataclass
from typing import List, Set

BOOST_WEIGHT = 0.3


def levenshtein(s1: str, s2: str) -> int:
    """Calculate the edit distance (Levenshtein distance) between two strings."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def prefix_score(query: str, target: str) -> float:
    """
    Calculate prefix match ratio between query and target.
    Returns 1.0 if target starts with query, otherwise returns
    the ratio of matching prefix characters to query length.
    """
    if not query:
        return 0.0

    if target.startswith(query):
        return 1.0

    # Count matching prefix characters
    match_len = 0
    for i, c in enumerate(query):
        if i < len(target) and target[i] == c:
            match_len += 1
        else:
            break

    return match_len / len(query)


SDK_PREFIXES = ('@ohos', '@kit', '@system', '@hms', '@native', '@ark')


def extract_keywords(module_path: str) -> Set[str]:
    """
    Extract meaningful keywords from a module path.

    Example: '@kit.ArkWeb.webview' -> {'arkweb', 'webview'}
    Example: '@ohos.web.webview.webview' -> {'web', 'webview'}
    Example: '@ohos.inputMethod.inputMethod' -> {'inputmethod'}
    """
    # Split by '.', convert to lowercase for case-insensitive matching
    parts = [p.lower() for p in module_path.split('.')]
    # Filter out SDK prefixes and single-char parts
    keywords = {p for p in parts if p and p not in SDK_PREFIXES and len(p) > 1}
    return keywords


@dataclass
class Recommendation:
    item: str
    member_name: str
    levenshtein_dist: int
    prefix_score: float
    combined_score: float
    source: str


def recommend_module(module_query: str, indexer, top_n: int = 3) -> List[Recommendation]:
    """
    Search all SDK module names and return recommendations sorted by combined score.

    Args:
        module_query: The module name query (e.g., "@ohos.app.ability.Abiity")
        indexer: SDKIndexer instance with loaded modules
        top_n: Maximum number of recommendations to return

    Returns:
        List of Recommendation objects sorted by combined_score descending
    """
    seen = {}
    query_part = module_query.rsplit('.', 1)[-1] if '.' in module_query else module_query

    for mod_name in indexer.get_module_list():
        mod_part = mod_name.rsplit('.', 1)[-1] if '.' in mod_name else mod_name
        dist = levenshtein(query_part, mod_part)
        max_len = max(len(query_part), len(mod_part))
        norm_dist = dist / max_len if max_len > 0 else 0
        prefix = prefix_score(query_part, mod_part)
        combined = max(1 - norm_dist, prefix)

        rec = Recommendation(
            item=mod_name,
            member_name=mod_part,
            levenshtein_dist=dist,
            prefix_score=prefix,
            combined_score=combined,
            source=mod_name
        )

        if mod_part not in seen or combined > seen[mod_part].combined_score:
            seen[mod_part] = rec

    sorted_recs = sorted(seen.values(), key=lambda r: r.combined_score, reverse=True)
    return sorted_recs[:top_n]


def recommend(member_name: str, indexer, top_n: int = 3, context_module: str = None) -> List[Recommendation]:
    """
    Search all SDK members and return recommendations sorted by combined score.

    Combined score = max((1 - dist/max_len), prefix_score)
    Deduplicated by member_name (keeping highest combined score).

    Args:
        member_name: The query string to search for
        indexer: SDKIndexer instance with loaded modules
        top_n: Maximum number of recommendations to return
        context_module: Optional module path to provide semantic context for boosting (e.g., "@kit.ArkWeb")

    Returns:
        List of Recommendation objects sorted by combined_score descending
    """
    seen_members = {}  # member_name -> Recommendation (keep highest combined)

    for module_name, module_info in indexer.modules.items():
        for class_name, class_info in module_info.classes.items():
            for member in class_info.members:
                dist = levenshtein(member_name, member)
                max_len = max(len(member_name), len(member))
                # Avoid division by zero
                norm_dist = dist / max_len if max_len > 0 else 0
                prefix = prefix_score(member_name, member)

                # Combined score as specified: max((1-dist/max_len), prefix)
                combined = max(1 - norm_dist, prefix)

                # Apply semantic context boost if context_module provided and keywords match
                if context_module:
                    context_kw = extract_keywords(context_module)
                    candidate_kw = extract_keywords(module_name)
                    if context_kw & candidate_kw:  # intersection non-empty
                        combined += BOOST_WEIGHT

                # source is the full member reference
                source = f"{module_name}.{class_name}.{member}"

                rec = Recommendation(
                    item=source,
                    member_name=member,
                    levenshtein_dist=dist,
                    prefix_score=prefix,
                    combined_score=combined,
                    source=source
                )

                # Dedupe by member_name, keeping highest combined score
                if member not in seen_members or combined > seen_members[member].combined_score:
                    seen_members[member] = rec

    # Sort by combined_score descending
    sorted_recs = sorted(seen_members.values(), key=lambda r: r.combined_score, reverse=True)

    return sorted_recs[:top_n]
