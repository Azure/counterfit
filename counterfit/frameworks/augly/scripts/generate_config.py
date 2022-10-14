import re
import yaml
import argparse
import importlib
import inspect

from counterfit.core.utils import get_subclasses

def generate_configs():
    base_import = importlib.import_module("augly.image.transforms")
    
    attacks = get_subclasses(base_import.BaseTransform)
    
    for attack_class in attacks[1:]:
        attack_name = re.findall(
            r"\w+", str(attack_class).split(".")[-1].strip())[0]
        attack_category = "common-corruption"
        attack_type = "blackbox"
        attack_data_tags = ["image"]

        params = {}   
        for k, v in inspect.signature(attack_class.__init__).parameters.items():
            if k == 'self' or k == 'kwargs' or k == 'aug_function':
                continue
            else:
                try:
                    if "Users" in v.default:
                        new_param = v.default.split("\\")[-1]
                except:
                    new_param = v.default
                
                params[k] = {
                    "docs": "Refer to attack file",
                    "default": new_param,
                    "optimize": {}
                }

        attack = {
            "attack_name": attack_name,
            "attack_docs": attack_class.apply_transform.__doc__,
            "attack_class": re.findall(r'augly\.image\.transforms\.\w+', str(attack_class))[0],
            "attack_type": attack_type,
            "attack_category": attack_category,
            "attack_data_tags": attack_data_tags,
            "attack_parameters": params
        }

        try:
            with open(f"../attacks/{attack_name}.yml", "w") as f:
                yaml.safe_dump(attack, f, sort_keys=True, indent=2)
        except Exception as error:
            print(error)
            continue

def main(args):
	generate_configs()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--generate", "-g", help="Generate base attack configurations for TextAttack")
	args = parser.parse_args()

	main(args)


