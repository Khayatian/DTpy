import os
from pathlib import Path
import yaml
from typing import Dict, Any, Union


def load_config(cfg_file_name) -> Dict[str, Any]:
    """Loads the config and parses to Dictionary."""
    with open(cfg_file_name, "r", encoding="utf-8") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)
    return cfg


def convert_entries_to_abs_pathes(config_dict: Dict[str, Any], basepath: str) -> None:
    """Converts all paths in the config to absolute paths."""
    for key, value in config_dict.items():
        if isinstance(value, dict):
            convert_entries_to_abs_pathes(config_dict[key], basepath)
        else:
            if isinstance(value, str):
                key_keywords = ["PATH", "FILE", "path", "file", "DIR", "dir", "FOLDER", "folder", "IDD"]
                value_keywords = [".csv", ".idf", ".txt", ".xls", ".xlsx", ".epw", ".yml", ".fmu", ".h5"]
                if "REL" not in key and "rel" not in key:
                    if any(([True if keyword in key else False for keyword in key_keywords])) or any(([True if keyword in value else False for keyword in value_keywords])):
                        if "$nestli$" in value:
                            config_dict[key] = abs_path(value[8:], Path(__file__).parent.parent.absolute())
                        else:
                            config_dict[key] = abs_path(value, basepath)


def abs_path(path: Union[str, Path], basepath: Union[str, Path]) -> str:
    """Converts a relative path to an absolute by using basepath as base. If path is already absolute, it returns the original path."""
    if os.path.exists(path):
        return str(os.path.abspath(path))
    elif os.path.isabs(path):
        return str(path)
    else:
        if os.path.isfile(basepath):
            basepath = os.path.abspath(os.path.dirname(basepath))
        return str(basepath / Path(path))


def validate_config(cfg: Dict):
    """Validates a config by checking if some constraints are met."""
    if "START" not in cfg or "DURATION" not in cfg or "RESOLUTION" not in cfg:
        raise LookupError("Config is missing key properties. Make sure you include START, DURATION, RESOLUTION")
