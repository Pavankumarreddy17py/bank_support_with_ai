import os
import sys
import json

# Ensure project root is on sys.path for imports like `backend` during tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Simple in-memory collector for test metrics
test_reports = []

def pytest_configure(config):
    # dict to allow tests to attach custom metrics keyed by nodeid
    config._test_metrics = {}

import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Collect test result after call phase
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        nodeid = item.nodeid
        metrics = item.config._test_metrics.get(nodeid)
        test_reports.append({
            'test': nodeid,
            'outcome': report.outcome,
            'duration': getattr(report, 'duration', None),
            'metrics': metrics,
        })


def pytest_sessionfinish(session, exitstatus):
    # Write report JSON into tests directory
    out_path = os.path.join(os.path.dirname(__file__), 'test_report.json')
    try:
        with open(out_path, 'w') as f:
            json.dump(test_reports, f, indent=2)
        print('\nWrote test report to:', out_path)
    except Exception as e:
        print('Failed to write test report:', e)
