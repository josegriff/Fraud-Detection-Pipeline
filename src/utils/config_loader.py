"""
This scirpt provides a safe utility to load configuration settings:
1. Reads a YAML configuration file from the specified path
2. yaml.safe_load used for secure parsing
3. Returns the configuration as a dictionary for the ETL pipeline
4. Used by the main orchestrator to access paths and other pipeline settings
"""

import yaml
from pathlib import Path

def load_config(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)
    