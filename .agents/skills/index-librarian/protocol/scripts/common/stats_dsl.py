"""
Stats DSL parser and evaluator.

Design authority: index-schema.md §3.1
Execution authority: THIS FILE.

Supported syntax (restricted — not arbitrary code):
  count(*)                            → count all children
  count(field != null)                → field exists
  count(field == null)                → field absent
  count(field == 'value')             → field equals value
  count(field != 'value')             → field not equals value
  count(f1 != null OR f2 != null)     → OR combination (max 2 conditions)
  count(f1 == null AND f2 == null)    → AND combination (max 2 conditions)
"""

import re
from typing import Any

from .frontmatter import get_nested


class DSLError(Exception):
    """Raised when a DSL expression is invalid."""
    pass


# Pattern: count(...)
COUNT_RE = re.compile(r"^count\((.+)\)$", re.DOTALL)

# Condition patterns
STAR_RE = re.compile(r"^\*$")
FIELD_NULL_RE = re.compile(r"^([\w.]+)\s*(==|!=)\s*null$")
FIELD_VALUE_RE = re.compile(r"^([\w.]+)\s*(==|!=)\s*'([^']*)'$")
COMBO_RE = re.compile(
    r"^([\w.]+)\s*(==|!=)\s*(null|'[^']*')\s+(AND|OR)\s+([\w.]+)\s*(==|!=)\s*(null|'[^']*')$"
)


def _parse_single_condition(expr: str):
    """Parse a single condition into a callable predicate."""
    expr = expr.strip()

    if STAR_RE.match(expr):
        return lambda meta: True

    m = FIELD_NULL_RE.match(expr)
    if m:
        field, op = m.group(1), m.group(2)
        if op == "!=":
            return lambda meta, f=field: get_nested(meta, f) is not None
        else:
            return lambda meta, f=field: get_nested(meta, f) is None

    m = FIELD_VALUE_RE.match(expr)
    if m:
        field, op, value = m.group(1), m.group(2), m.group(3)
        if op == "==":
            return lambda meta, f=field, v=value: str(get_nested(meta, f, "")) == v
        else:
            return lambda meta, f=field, v=value: str(get_nested(meta, f, "")) != v

    raise DSLError(f"Invalid condition: {expr}")


def _parse_value(raw: str):
    """Parse 'null' or quoted string."""
    raw = raw.strip()
    if raw == "null":
        return None
    if raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1]
    raise DSLError(f"Invalid value: {raw}")


def parse_rule(rule: str):
    """Parse a DSL rule string into a predicate function.

    Args:
        rule: DSL expression string (e.g., "count(field != null)")

    Returns:
        A callable that takes a list of metadata dicts and returns an int count.
    """
    rule = rule.strip()
    m = COUNT_RE.match(rule)
    if not m:
        raise DSLError(f"Rule must be count(...), got: {rule}")

    inner = m.group(1).strip()

    # Check for compound condition (AND/OR)
    cm = COMBO_RE.match(inner)
    if cm:
        f1, op1, v1_raw, logic, f2, op2, v2_raw = cm.groups()
        v1 = _parse_value(v1_raw)
        v2 = _parse_value(v2_raw)

        def _check_field(meta: dict, field: str, op: str, val: Any) -> bool:
            actual = get_nested(meta, field)
            if val is None:
                return (actual is None) if op == "==" else (actual is not None)
            return (str(actual) == str(val)) if op == "==" else (str(actual) != str(val))

        if logic == "AND":
            pred = lambda meta, _f1=f1, _o1=op1, _v1=v1, _f2=f2, _o2=op2, _v2=v2: (
                _check_field(meta, _f1, _o1, _v1)
                and _check_field(meta, _f2, _o2, _v2)
            )
        else:  # OR
            pred = lambda meta, _f1=f1, _o1=op1, _v1=v1, _f2=f2, _o2=op2, _v2=v2: (
                _check_field(meta, _f1, _o1, _v1)
                or _check_field(meta, _f2, _o2, _v2)
            )

        return lambda children, p=pred: sum(1 for c in children if p(c))

    # Single condition
    pred = _parse_single_condition(inner)
    return lambda children, p=pred: sum(1 for c in children if p(c))


def evaluate_stats_schema(
    stats_schema: dict, children_metadata: list[dict]
) -> dict[str, int]:
    """Evaluate a stats_schema against children metadata.

    Args:
        stats_schema: Dict of {bucket_name: {rule: "count(...)", type: "...", ...}}
        children_metadata: List of frontmatter dicts from child nodes.

    Returns:
        Dict of {bucket_name: count_value}
    """
    result = {}
    for bucket_name, schema_entry in stats_schema.items():
        if isinstance(schema_entry, dict):
            rule = schema_entry.get("rule", "")
        elif isinstance(schema_entry, str):
            # Simple format: bucket_name: "description" (no rule, skip)
            continue
        else:
            continue

        if not rule:
            continue

        try:
            counter = parse_rule(rule)
            result[bucket_name] = counter(children_metadata)
        except DSLError:
            # Skip invalid rules, let verify catch them
            pass

    return result
