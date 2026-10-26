import ast
import json
import os
from pathlib import Path

import pytest

NOTEBOOK = Path(__file__).resolve().parents[1] / 'notebooks/evidence_audit.ipynb'


def cells():
    return [''.join(c['source']) for c in json.loads(NOTEBOOK.read_text())['cells'] if c['cell_type'] == 'code']


def test_notebook_compiles_and_uses_its_own_key():
    code = cells()
    for source in code:
        compile(source, str(NOTEBOOK), 'exec')
    assert "userdata.get('COLLUSION_F2_KEY')" in code[0]
    assert "COLLUSION_OPENROUTER_API_KEY" not in ''.join(code) and "userdata.get('OPENROUTER_API_KEY')" not in ''.join(code)


def test_key_check_rejects_a_key_above_the_f2_allocation():
    source = next(c for c in cells() if 'def check_key_budget' in c)
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'check_key_budget')
    scope = {}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(NOTEBOOK), 'exec'), scope)  # noqa: S102
    assert scope['check_key_budget']({'limit': 10, 'limit_remaining': 10, 'limit_reset': None})['key_limit_usd'] == 10
    with pytest.raises(RuntimeError, match='separate F2 key'):
        scope['check_key_budget']({'limit': 100, 'limit_remaining': 100, 'limit_reset': None})  # e.g. the main key


def test_paid_cell_blocked_before_offline_and_budget_checks():
    launch = next(c for c in cells() if 'def run_family' in c)
    first = ast.Module(body=[ast.parse(launch).body[0]], type_ignores=[])
    for state in ({}, {'OFFLINE_PASSED': True}, {'BUDGET_VERIFIED': True}):
        with pytest.raises(RuntimeError, match='Offline controls'):
            exec(compile(first, str(NOTEBOOK), 'exec'), state)  # noqa: S102 - exercise our local notebook gate
    assert "command('canary', 60)" in launch
    assert launch.index('if not all(checks.values())') < launch.index("command('pilot', 500)")


def test_scientific_control_failure_prevents_offline_pass():
    offline = next(c for c in cells() if 'scripts/check_covert_controls.py' in c)
    calls = []

    def sh(command, **kwargs):  # same signature as the setup cell's sh
        calls.append(command)
        if 'scripts/check_covert_controls.py' in command:
            raise RuntimeError('injected scientific control failure')

    from types import SimpleNamespace
    state = {'sh': sh, 'os': os, 'sys': SimpleNamespace(executable='python'), 'OUT': Path('/tmp'), 'FAMILIES': []}
    with pytest.raises(RuntimeError, match='scientific control'):
        exec(compile(offline, str(NOTEBOOK), 'exec'), state)  # noqa: S102 - exercise our local notebook gate
    assert state['OFFLINE_PASSED'] is False
    assert not any('sprint.covert_run' in command for command in calls)
