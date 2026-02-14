import types
from datetime import datetime, timedelta

import pytest
import sys
import pathlib

# ensure repo root is on sys.path for imports
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

# Provide a lightweight fake for actions.nmap_vuln_scanner to avoid heavy deps during tests
import types
fake_nmap_mod = types.ModuleType('actions.nmap_vuln_scanner')
class _FakeNmap:
    def __init__(self, shared):
        self.shared = shared
    def execute(self, *args, **kwargs):
        return 'success'
fake_nmap_mod.NmapVulnScanner = _FakeNmap
sys.modules['actions.nmap_vuln_scanner'] = fake_nmap_mod

# Provide a fake init_shared with a lightweight shared_data to avoid running
# the real hardware initialization in tests
from types import ModuleType
fake_init = ModuleType('init_shared')
fake_init.shared_data = None  # will be set later in helper
sys.modules['init_shared'] = fake_init

from orchestrator import Orchestrator


class FakeSharedData:
    def __init__(self):
        self.retry_success_actions = False
        self.success_retry_delay = 60
        self.failed_retry_delay = 30
        self.scan_interval = 10
        self.orchestrator_should_exit = True
        self.max_workers = 2
        self._last_written = None

    def write_data(self, data):
        self._last_written = data

    def read_data(self):
        return []


class FakeAction:
    def __init__(self, name, port, result='success'):
        self.action_name = name
        self.port = port
        self.b_parent_action = None
        self._result = result

    def execute(self, ip=None, port=None, row=None, action_key=None):
        return self._result


def make_orchestrator_with_shared(shared):
    # instantiate without running __init__ to avoid loading real actions
    orch = Orchestrator.__new__(Orchestrator)
    orch.shared_data = shared
    orch.actions = []
    orch.standalone_actions = []
    orch.failed_scans_count = 0
    orch.network_scanner = None
    orch.last_vuln_scan_time = datetime.min
    orch.semaphore = None
    import threading, concurrent.futures
    orch.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    orch.data_lock = threading.Lock()
    return orch


def test_execute_action_success_updates_row_and_writes():
    shared = FakeSharedData()
    orch = make_orchestrator_with_shared(shared)
    action = FakeAction('TestAction', port=22, result='success')
    row = {'MAC Address': 'AA:BB', 'IPs': '192.0.2.1', 'Ports': '22;80', 'Alive': '1'}
    current_data = [row]

    res = orch.execute_action(action, '192.0.2.1', ['22', '80'], row, 'TestAction', current_data)
    assert res is True
    assert row['TestAction'].startswith('success_')
    assert shared._last_written is not None


def test_execute_action_skips_on_recent_success_when_retry_disabled():
    shared = FakeSharedData()
    shared.retry_success_actions = False
    orch = make_orchestrator_with_shared(shared)
    action = FakeAction('TestAction', port=22, result='success')
    timestamp = (datetime.now() - timedelta(seconds=10)).strftime("%Y%m%d_%H%M%S")
    row = {'MAC Address': 'AA:BB', 'IPs': '192.0.2.1', 'Ports': '22;80', 'Alive': '1', 'TestAction': f'success_{timestamp}'}
    current_data = [row]

    res = orch.execute_action(action, '192.0.2.1', ['22', '80'], row, 'TestAction', current_data)
    assert res is False


def test_execute_standalone_action_runs_and_writes():
    shared = FakeSharedData()
    orch = make_orchestrator_with_shared(shared)
    action = FakeAction('Standalone', port=0, result='success')
    # empty current_data should create a STANDALONE row
    current_data = []

    res = orch.execute_standalone_action(action, current_data)
    assert res is True
    # Ensure STANDALONE row exists
    standalone_row = next((r for r in current_data if r.get('MAC Address') == 'STANDALONE'), None)
    assert standalone_row is not None
    assert standalone_row['Standalone'].startswith('success_')
    assert shared._last_written is not None
