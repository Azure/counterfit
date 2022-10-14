from abc import abstractmethod

class CFFramework:
    """Base class for all frameworks. This class enforces standard functions used by Counterfit.
    """

    @abstractmethod
    def build(self, target, attack):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def pre_attack_processing(self, cfattack):
        pass

    @abstractmethod
    def post_attack_processing(self, cfattack):
        pass

    @abstractmethod
    def set_parameters(self, cfattack):
        pass

    def get_attack(attack_name: str) -> object:
        """Get an attack stored in `framework.attacks`

        Args:
            attack_name (str): The name (key value) of the attack.

        Returns:
            object: The attack.
        """
