from configparser import ConfigParser
import os
import json


config_path = "config/config.ini"
config_parser = ConfigParser()
config_parser.optionxform = str  # To preserve the case

config = {}


def init_config():
    global config

    # Expected sections:
    # - MY_CONF_SECTION_1
    # - MY_CONF_SECTION_2

    print("======================== CONFIG ===========================")

    # First, read the config file
    config_parser.read(config_path)
    config = {
        "MY_CONF_SECTION_1": {"CONF_ELEMENT_1": True, "CONF_ELEMENT_2": "Hello World!"},
        "MY_CONF_SECTION_2": {"CONF_ELEMENT_3": 10000},
    }

    for section in config_parser.sections():
        # Data providers
        if section == "MY_CONF_SECTION_1":
            if "CONF_ELEMENT_1" in config_parser[section]:
                if str.lower(config_parser[section]["CONF_ELEMENT_1"]) == "false":
                    print("Config file: Data Providers creation disabled")
                    config["MY_CONF_SECTION_1"]["CONF_ELEMENT_1"] = False

            if "CONF_ELEMENT_2" in config_parser[section]:
                config["MY_CONF_SECTION_1"]["CONF_ELEMENT_2"] = config_parser[section][
                    "CONF_ELEMENT_2"
                ]
            continue

        if section == "MY_CONF_SECTION_2":
            if "CONF_ELEMENT_3" in config_parser[section]:
                config["MY_CONF_SECTION_2"]["CONF_ELEMENT_3"] = int(
                    config_parser[section]["CONF_ELEMENT_3"]
                )
            continue

        print("Config section '" + section + "' not recognized, skipping")

    # Then deal with environment variables
    # Refer to the config.env file to see the expected environment variables
    for env_var in os.environ:
        # Deal with MY_CONF_SECTION_1 in env variables
        if env_var == "ALGO_CONF_ELEMENT_1":
            # Env var format: ALGO_CONF_ELEMENT_1=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: conf element 1 disabled")
                config["MY_CONF_SECTION_1"]["CONF_ELEMENT_1"] = False
            continue

        if env_var == "ALGO_CONF_ELEMENT_2":
            # Env var format: ALGO_CONF_ELEMENT_2=<string>
            config["MY_CONF_SECTION_1"]["CONF_ELEMENT_2"] = os.environ[env_var]
            continue

        # Deal with MY_CONF_SECTION_2 in env variables
        if env_var == "ALGO_CONF_ELEMENT_3":
            # Env var format: ALGO_CONF_ELEMENT_3=<int>
            config["MY_CONF_SECTION_2"]["CONF_ELEMENT_3"] = int(os.environ[env_var])
            continue

    print("Config loaded")
    print(json.dumps(config, sort_keys=True, indent=4))


def get_config():
    return config
