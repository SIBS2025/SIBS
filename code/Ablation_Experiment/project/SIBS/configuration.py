import os
import json
import random
from typing import List

def read_config_file(file_path: str) -> List[str]:

    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {file_path}")
        return []
    except Exception as e:
        print(f"Unexpected error while reading config file: {e}")
        return []


def ensure_output_directory(directory: str) -> None:

    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created output directory: {directory}")


def is_conflicting_option(current_config: str, new_option: str) -> bool:

    if "--disable" in new_option and "--enable" in current_config:
        return new_option[5:] in current_config
    if "--enable" in new_option and "--disable" in current_config:
        return new_option[4:] in current_config
    if "--with" in new_option and "--without" in current_config:
        return new_option[6:] in current_config
    if "--without" in new_option and "--with" in current_config:
        return new_option[9:] in current_config
    return False


def generate_random_config(size: List[str], config_count: int, output_dir: str) -> None:

    for id in range(1, config_count + 1):
        config = str()
        num_options = random.randint(3, 5)
        for _ in range(num_options):
            random_index = random.randint(0, len(size) - 1)
            new_option = size[random_index]

            if new_option not in config and not is_conflicting_option(config, new_option):
                config = config + " " + new_option

        # Save the generated configuration as a JSON file
        config_filename = f"C{id} {config}.json"
        config_filepath = os.path.join(output_dir, config_filename)
        try:
            with open(config_filepath, "w") as json_file:
                json.dump(config.strip(), json_file)
            print(f"Configuration saved: {config_filepath}")
        except Exception as e:
            print(f"Error saving configuration file {config_filename}: {e}")


def generate_configs(base_dir,length):
  
    # Base directory and file paths
    config_file_path = os.path.join(base_dir, "configtxt/config.txt")
    output_dir = os.path.join(base_dir, "Json")

    # Ensure output directory exists
    ensure_output_directory(output_dir)

    # Read configuration options from the file
    config_options = read_config_file(config_file_path)
    if not config_options:
        print("No configuration options available. Exiting...")
        return

    # Generate random configurations
    generate_random_config(config_options, config_count=length, output_dir=output_dir)


# if __name__ == "__main__":
#     base_dir=""
#     generate_configs(base_dir,20)
