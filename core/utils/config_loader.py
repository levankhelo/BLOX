import os
import yaml

def load_config(config_file_path):
    with open(config_file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config
