import re
import yaml
import argparse
import importlib

from counterfit.core.utils import get_subclasses

def generate_configs():
    base_import = importlib.import_module(
        "textattack.attack_recipes")
    attacks = get_subclasses(base_import.AttackRecipe)
    
    for attack_class in attacks:
        attack_name = re.findall(
            r"\w+", str(attack_class).split(".")[-1].strip())[0]
        attack_category = "evasion"
        attack_type = "closed-box"
        attack_data_tags = ["text"]
        attack_params = {}   

        attack = {
            "attack_name": attack_class.__module__.split(".")[-1],
            "attack_docs": attack_class.__doc__,
            "attack_class": re.findall(r'textattack\.attack_recipes\.\w+.\w+', str(attack_class))[0],
            "attack_type": attack_type,
            "attack_category": attack_category,
            "attack_data_tags": attack_data_tags,
            "attack_parameters": attack_params
        }

        filename = attack_class.__module__.split(".")[-1]

        with open(f"../attacks/{filename}.yml", "w") as f:
            yaml.safe_dump(attack, f, sort_keys=True, indent=2)

def main(args):
	generate_configs()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--generate", "-g", help="Generate base attack configurations for TextAttack")
	args = parser.parse_args()

	main(args)


