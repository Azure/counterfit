import os 
import warnings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # make tensorflow quiet
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)



import pytest

from counterfit.core.state import CFState
from counterfit.core.utils import set_id

class TestArtFramework:

    @pytest.fixture(params=["creditfraud", "satellite", "digits_keras", "digits_blackbox"])
    def target(self, request):
        yield request.param

    @pytest.fixture(scope='function')
    def cfstate_state(self, target):
        cfstate = CFState.state()
        cfstate._init_state()
        cfstate.load_framework("art")
        cfstate.load_target(target)
        return cfstate

    # def test_build(self, cfstate_state, target):
    #     scan_id = set_id()
    #     cfattack_id = cfstate_state.build_new_attack(target, "HopSkipJump", scan_id)
        

    def test_build_run(self, cfstate_state, target):
        scan_id = set_id()
        cfattack_id = cfstate_state.build_new_attack(target , "HopSkipJump", scan_id)
        assert cfattack_id is not None

        attack_complete = cfstate_state.run_attack(target, cfattack_id)
        assert attack_complete is True

