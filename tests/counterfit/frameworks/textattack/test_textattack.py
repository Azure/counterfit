import pytest
from counterfit.core.state import CFState
from counterfit.core.utils import set_id

class TestTextAttackFramework:

    @pytest.fixture(params=["movie_reviews"])
    def target(self, request):
        yield request.param

    @pytest.fixture(scope='function')
    def cfstate_state(self, target):
        cfstate = CFState.state()
        cfstate._init_state()
        cfstate.load_framework("textattack")
        cfstate.load_target(target)
        return cfstate

    def test_build_run(self, cfstate_state, target):
        scan_id = set_id()
        cfattack_id = cfstate_state.build_new_attack(target, "DeepWordBugGao2018", scan_id)
        assert cfattack_id is not None

        attack_complete = cfstate_state.run_attack(target, cfattack_id)
        assert attack_complete is True

