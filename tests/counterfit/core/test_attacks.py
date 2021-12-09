# import datetime

# import pytest

# from counterfit.core.attacks import CFAttack


# class ConcreteAttack(Attack):
#     def attack_cls(self):
#         raise NotImplementedError

#     def attack_name(self):
#         raise NotImplementedError

#     def attack_type(self):
#         raise NotImplementedError

#     def category(self):
#         raise NotImplementedError

#     def framework(self):
#         raise NotImplementedError

#     def random(self):
#         raise NotImplementedError

#     def default(self):
#         raise NotImplementedError


# class TestAttack:

#     @pytest.fixture(scope='function')
#     def attack_handler(self):
#         attack_obj = ConcreteAttack()
#         attack_obj.attack_cls = 'TEMP_ATTACK_CLS'
#         attack_obj.attack_name = 'TEMP_ATTACK'
#         attack_obj.attack_type = 'TEMP_ATTACK_TYPE'
#         attack_obj.category = 'TEMP_CATEGORY'
#         attack_obj.framework = 'TEMP_FRAMEWORK'
#         attack_obj.random = 'RANDOM_PARAMS'
#         attack_obj.default = 'DEFAULT_PARAMS'
#         attack_obj.created_time = 'NOW'
#         attack_obj.attack_id = 'TEMP_ID'
#         attack_obj.sample_index = 'SAMPLE_IDX'
#         attack_obj.target_class = 'TARGET_CLASS'
#         attack_obj.parameters = 'TEMP_PARAMS'
#         attack_obj._logs = [{'TEMP_KEY': 'TEMP_VALUE'}]
#         return attack_obj

#     def test_set_attack_parameters(self, attack_handler):
#         params = {'default': 2.5}
#         expected_parameters = {'default': 2.5}
#         attack_handler.set_attack_parameters(params)
#         assert expected_parameters == attack_handler.parameters

#     def test_param_floats_to_ints(self, attack_handler):
#         params = {'a': 2.5, 'b': 3.0}
#         assert type(attack_handler._param_floats_to_ints(params)['b']) is int

#     def test_dump(self, attack_handler):
#         expected_keys = {'attack_name', 'created', 'attack_id',
#                          'sample_index', 'target_class', 'parameters', 'results', 'logs'}
#         assert expected_keys == set(attack_handler.dump().keys())

#     def test_append_log(self, attack_handler):
#         timestamp = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
#         target_name = 'TEMP_MODEL'
#         attack_name = 'TEMP_ATTACK'
#         attack_id = 'TEMP_ID'
#         input_data = [1.0, 2.0, 3.0]
#         output = [0.91, 0.09]
#         label = 1
#         log_entry = {
#             "timestamp": timestamp,
#             "model_id": target_name,
#             "attack_name": attack_name,
#             "attack_id": attack_id,
#             "input": input_data,
#             "output": output,
#             "label": label
#         }
#         attack_handler.append_log(log_entry)
#         attack_handler.append_log(log_entry)
#         assert len(attack_handler._logs) == 3
