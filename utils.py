import os
import yaml
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path 


@ensure_annotations
def read_yaml(path_to_yaml)-> ConfigBox: #reading yaml
    """
    Read a YAML file and return its contents as a ConfigBox.

    Args:
        path_to_yaml (str): The path to the YAML file.

    Returns:
        ConfigBox: The contents of the YAML file as a ConfigBox.

    Raises:
        ValueError: If the YAML file is empty.
        Exception: If an error occurs while reading the YAML file.
    """
    with open(path_to_yaml) as yaml_file:
        content=yaml.safe_load(yaml_file)
        return ConfigBox(content)
