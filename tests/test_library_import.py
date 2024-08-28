import pytest


def test_import_my_library():
    try:
        import agentic_workflows
    except ImportError as e:
        pytest.fail(f"Failed to import 'agentic_workflows': {e}")
