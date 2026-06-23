"""
Module checks auto-registration.

This package automatically discovers and registers check functions from
module-specific Python files in this directory.

Each module file (e.g., meetings.py) can define check_* functions that
index_verify.py will dynamically load and execute.
"""
