import re
import yaml
import argparse

from frameworks.art.utils import attack_factory, get_default_params, load_attacks, attack_tags, attacks_still_wip, attack_types

def generate_configs():

    # Get available attack in ART
	attacks = load_attacks()
        
	for k, v in attacks.items():
		if k in attacks_still_wip:
			continue

		loaded_attack = attack_factory(v)
		default_params = get_default_params(loaded_attack)

		attack_docs = re.findall(r"\:param\s(\w+)\:\s+(\w+.*)", loaded_attack.__init__.__doc__)

		docs = {}
		for i in attack_docs:
			if i[0] in default_params.keys():
				docs[i[0]] = i[1]
			else:
				continue

		params = {}
		for k, v in default_params.items():
			optimize = {}
			type_v = type(v)
			if k == "norm":
				optimize["choice"] = ["inf"]
			elif type_v is bool:
				optimize["bool"] = {"true": True, "false": False}
			elif type_v is str:
				optimize["choice"] = [v]
			elif type_v is int:
				optimize["uniform"] = {"min": 1, "max": 200}
			elif type_v is float:
				optimize["discrete"] = {"min": 0.01, "max": 1.0}
			elif type_v is tuple:
				optimize["uniform"] = [*v]
				v = [*v]
			params[k] = {
				"docs": docs.get(k, "Refer to attack file."),
				"default": v,
				"optimize": optimize
			}

		# category
		attack_attributes = loaded_attack.__dir__()

		if "generate" in attack_attributes:
			attack_category = "evasion"
		elif "infer" in attack_attributes:
			attack_category = "inference"
		elif "reconstruct" in attack_attributes:
			attack_category = "inversion"
		elif "extract" in attack_attributes:
			attack_category = "inversion"
		elif "poison" or "poison_estimator" in attack_attributes:
			attack_category = "poison"
		else:
			attack_category = "unknown"

		# data tags
		if loaded_attack.__class__.__name__ in attack_tags.keys():
			attack_data_tags = attack_tags[loaded_attack.__class__.__name__]
		else:
			attack_data_tags = []
			

		# type
		if loaded_attack.__class__.__name__ in attack_types.keys():
			attack_type = attack_types[loaded_attack.__class__.__name__]
		else:
			attack_type = "unknown"


		attack = {
			"attack_name": loaded_attack.__module__.split(".")[-1],
			"attack_docs": loaded_attack.__doc__,
			"attack_class": f"{loaded_attack.__module__}.{loaded_attack.__class__.__name__}",
			"attack_type": attack_type,
			"attack_category": attack_category,
			"attack_data_tags": attack_data_tags,
			"attack_parameters": params
		}

		filename = loaded_attack.__module__.split(".")[-1]

		with open(f"counterfit/frameworks/art/attacks/{filename}.yml", "w") as f:
			yaml.safe_dump(attack, f, sort_keys=True, indent=2)

def main(args):
	generate_configs()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--generate", "-g", help="Generate base attack configurations for ART")
	args = parser.parse_args()

	main(args)


