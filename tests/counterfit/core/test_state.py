from collections import defaultdict
import pytest
from unittest.mock import Mock

from counterfit.core.state import CFState


class TestCFState:
    
    @pytest.fixture(scope='function')
    def target_singleton_handler(self):
        target_singleton_obj = CFState.get_instance()
        return target_singleton_obj
    
    def test_singleton_obj(self, target_singleton_handler):
        a = target_singleton_handler
        b = CFState.get_instance()
        assert a == b
    
    def test_set_active_target(self, target_singleton_handler):
        target_singleton_handler.loaded_targets['TEMP_MODEL_NAME'] = Mock()
        target_singleton_handler.set_active_target('TEMP_MODEL_NAME')
        assert target_singleton_handler.active_target._mock_parent == None
    
    def test_set_active_attack(self, target_singleton_handler):
        target_singleton_handler.active_target = Mock()
        target_singleton_handler.active_target.attacks = defaultdict()
        target_singleton_handler.active_target.attacks['TEMP_ATTACK_ID'] = Mock()
        target_singleton_handler.set_active_attack('TEMP_ATTACK_ID')
        assert target_singleton_handler.active_target.active_attack._mock_new_name == 'active_attack'
    
    def test_load_attack(self, target_singleton_handler):
        attack_obj = Mock()
        attack_obj.attack_name = 'TEMP_ATTACK'
        target_singleton_handler.load_attack(attack_obj)
        assert 'TEMP_ATTACK' in target_singleton_handler.loaded_attacks
