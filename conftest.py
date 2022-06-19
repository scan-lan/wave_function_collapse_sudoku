from typing import Iterable, Literal
import pytest


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--run-success-rate", action="store_true", default=False,
                     help="run tests showing success rate of grid generation")
    parser.addoption("--run-performance", action="store_true", default=False,
                     help="run performance tests")


def pytest_configure(config: pytest.Config):
    config.addinivalue_line("markers", "success_rate: mark test as a success rate test")
    config.addinivalue_line("markers", "performance: mark test as a performance test")


def pytest_collection_modifyitems(config: pytest.Config, items: Iterable[pytest.Item]):
    run_success_rate = config.getoption("--run-success-rate")
    run_performance = config.getoption("--run-performance")
    run_type_markers = {"success_rate": {True: pytest.mark.skip(reason="used option --run-success-rate"),
                                         False: pytest.mark.skip(reason="need --run-success-rate option to run")},
                        "performance": {True: pytest.mark.skip(reason="used option --run-performance"),
                                        False: pytest.mark.skip(reason="need --run-performance option to run")}}
    run_type: Literal["success_rate", "performance", None] = None
    if run_performance:
        run_type = "performance"
    elif run_success_rate:
        run_type = "success_rate"

    if run_type is None:
        for item in items:
            for run_type_key in run_type_markers.keys():
                if run_type_key in item.keywords:
                    item.add_marker(run_type_markers[run_type_key][False])
    else:
        for item in items:
            if run_type not in item.keywords:
                item.add_marker(run_type_markers[run_type][True])
