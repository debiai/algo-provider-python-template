import config.init_config as config


def init():
    # Init config file
    config.init_config()
    conf = config.get_config()
    conf_element_1 = conf["MY_CONF_SECTION_1"]["CONF_ELEMENT_1"]
    conf_element_2 = conf["MY_CONF_SECTION_1"]["CONF_ELEMENT_2"]
    conf_element_3 = conf["MY_CONF_SECTION_2"]["CONF_ELEMENT_3"]
    print(conf_element_1, conf_element_2, conf_element_3)

    # Init what you need here
    # ...
