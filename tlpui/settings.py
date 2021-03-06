import configparser, re, sys
from subprocess import check_output
from os import path, getenv
from pathlib import Path

# application folder settings
workdir = path.dirname(path.abspath(__file__))
langdir = workdir + '/lang/'
icondir = workdir + '/icons/'

# default user params
language = 'en_EN'
tlpconfigfile = '/etc/default/tlp'
activecategorie = 0
windowxsize = 900
windowysize = 600

# user config
userconfighome = getenv("XDG_CONFIG_HOME")
if userconfighome == "": 
	userconfigpath = Path(str(Path.home()) + "/.config/tlpui")
else:
	userconfigpath = Path(str(userconfighome) + "/tlpui")
userconfigfile = Path(str(userconfigpath) + "/tlpui.cfg")


def persist():
    config = configparser.ConfigParser()
    config.read_file(open(str(userconfigfile)))
    config['default']['language'] = language
    config['default']['tlpconfigfile'] = tlpconfigfile
    config['default']['activecategorie'] = str(activecategorie)
    config['default']['windowxsize'] = str(windowxsize)
    config['default']['windowysize'] = str(windowysize)
    with open(str(userconfigfile), 'w') as configfile:
        config.write(configfile)


def get_setting_file() -> str:
    pattern = re.compile(r"Configured Settings: ([^\s]+)")
    currentconfig = check_output(["tlp-stat", "-c"]).decode(sys.stdout.encoding)
    matcher = pattern.search(currentconfig)
    return matcher.group(1)


def get_installed_tlp_version() -> str:
    pattern = re.compile(r"TLP ([^\s]+)")
    currentconfig = check_output(["tlp-stat", "-c"]).decode(sys.stdout.encoding)
    matcher = pattern.search(currentconfig)
    version = matcher.group(1).replace(".", "_")
    return version


if userconfigfile.exists():
    config = configparser.ConfigParser()
    config.read_file(open(str(userconfigfile)))
    tlpconfigfile = config['default']['tlpconfigfile']
    language = config['default']['language']
    activecategorie = int(config['default']['activecategorie'])
    windowxsize = int(config['default']['windowxsize'])
    windowysize = int(config['default']['windowysize'])
else:
    userconfigpath.mkdir(parents=True, exist_ok=True)
    userconfigfile.touch()
    userconfigfile.write_text("[default]")
    tlpconfigfile = get_setting_file()
    persist()


# runtime params
tlpconfig = dict()
tlpconfig_original = dict()
imagestate = dict()
