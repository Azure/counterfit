from collections import defaultdict
import pytest
from unittest.mock import Mock

from counterfit.core.config import Config
from counterfit.core.state import CFState
from counterfit.core.frameworks import Framework


class TestCFState:

    @pytest.fixture(scope='function')
    def cfstate_state(self):
        cfstate = CFState.state()
        return cfstate

    def test_singleton_obj(self, cfstate_state):
        a = cfstate_state
        b = CFState.state()
        assert a == b

    def test_import_frameworks(self, cfstate_state):
        cfstate_state.import_frameworks(
            frameworks_path="counterfit/frameworks")
        assert len(cfstate_state.frameworks) > 0

    def test_add_framework(self, cfstate_state):
        cfstate_state.add_framework(framework_name="test", framework=Mock())
        assert "test" in cfstate_state.frameworks.keys()

    def test_load_framework(self, cfstate_state):
        cfstate_state.load_framework(
            framework="art", force_no_config=False)
        assert cfstate_state.frameworks["art"].attacks is not None

    def test_get_frameworks(self, cfstate_state):
        assert cfstate_state.frameworks is not None

    def test_reload_framework(self, cfstate_state):
        cfstate_state.reload_framework(framework_name="art")
        assert cfstate_state.frameworks["art"] is not None

    def test_import_targets(self, cfstate_state):
        cfstate_state.import_targets(targets_path="counterfit/targets")
        assert len(cfstate_state.targets) > 0

    def test_add_target(self, cfstate_state):
        cfstate_state.add_target(target_name="test_target", target=Mock())
        assert cfstate_state.targets["test_target"] is not None

    def test_load_target(self, cfstate_state):
        cfstate_state.load_target("test_target")

    def test_reload_target(self, cfstate_state):
        pass

    def test_list_targets(self):
        pass

    def test_get_attacks(self):
        pass

    def test_get_active_target(self):
        pass

    def test_add_attack_to_target(self, cfstate_state):
        pass

    def test_build_new_attack(self, cfstate_state):
        pass

    def test_run_attack(self, cfstate_state):
        pass

    def test_set_active_target(self, cfstate_state):
        pass

    def test_set_active_target(self, cfstate_state):
        cfstate_state.targets['TEMP_target_name'] = Mock()
        cfstate_state.set_active_target(Mock)
        assert cfstate_state.active_target == Mock
