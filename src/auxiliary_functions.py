from configparser import ConfigParser
from config import MAIN_CONFIG_PATH


# CONFIGS block
def read_config(config_path: str):
    """ Return config as ConfigParser obj. and content as string (content of the config). """
    config = ConfigParser()

    file = open(config_path, 'r', encoding='utf-8')
    content = file.read()
    file.close()
    config.read(config_path, encoding='utf-8')

    return config, content


def update_config(config_path: str, commands: str):
    config = ConfigParser()

    text = commands.split('\n')
    failures = []
    for line in text:
        if len(line.split(' ')) < 3:
            failures.append(line)
            continue

        config.read(config_path, encoding='utf-8')
        section, variable = line.split(' ')[:2]
        value = ' '.join(line.split(' ')[2:])
        if ' ' in section or ' ' in variable or section not in config.sections():
            failures.append(line)
            continue

        config[section][variable] = value
        with open(config_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

    return failures


def load_default_config(config_path: str):
    default_config_path = config_path.split('/')
    default_config_path = 'AppData/defaults/default_' + default_config_path[-1]

    default = open(default_config_path, 'r', encoding='utf-8')
    default_settings = default.read()
    default.close()
    user_config = open(config_path, 'w', encoding='utf-8')
    user_config.write(default_settings)
    user_config.close()
