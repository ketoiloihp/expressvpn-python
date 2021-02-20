import random
import subprocess
import re

from expressvpn.commands import *


class ConnectException(Exception):
    pass


def run_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    return list([str(v).replace('\\t', ' ').replace('\\n', ' ').replace('b\'', '').replace('\'', '')
                .replace('b"', '')
                 for v in iter(p.stdout.readline, b'')])


def activation_check():
    print('Checking if the client is activated... (Please wait)')
    out = connect()
    if not is_activated(out):
        print('Please run <expressvpn activate> and provide your activation key. Program will exit.')
        exit(1)
    print('Client is successfully logged in.')
    disconnect()


def connect():
    return run_command(VPN_CONNECT)


def disconnect():
    return run_command(VPN_DISCONNECT)


def is_activated(connect_output):
    return not check_if_string_is_in_output(connect_output, 'Please activate your account')


def check_if_string_is_in_output(out, string):
    for item in out:
        if string in item:
            return True
    return False


def print_output(out):
    for o in out:
        print('- {}'.format(o))


def connect_alias(alias):
    command = VPN_CONNECT + ' -c --random "' + str(alias) +'"' if IS_MAC else VPN_CONNECT + ' ' + str(alias)
    print(command)
    out = run_command(command)
    if check_if_string_is_in_output(out, 'We were unable to connect to this VPN location'):
        raise ConnectException()
    if check_if_string_is_in_output(out, 'not found'):
        raise ConnectException()
    print('Successfully connected to {}'.format(alias))


def extract_aliases(vpn_list):
    try:
        return extract_aliases_1(vpn_list)
    except:
        return extract_aliases_3(vpn_list) if IS_MAC else extract_aliases_2(vpn_list)


def extract_aliases_1(vpn_list):
    """
    - ALIAS COUNTRY     LOCATION   RECOMMENDED
    - ----- ---------------    ------------------------------ -----------
    """
    aliases = []
    for vpn_item in vpn_list[2:]:
        alias = vpn_item.split()[0]
        aliases.append(alias)
    return aliases

def extract_aliases_2(vpn_list):
    """
    Recommended locations:
    - ALIAS COUNTRY     LOCATION   RECOMMENDED
    - ----- ---------------    ------------------------------ -----------
    """
    aliases = []
    for vpn_item in vpn_list[3:]:
        try:
            alias = vpn_item.split()[0]
            aliases.append(alias)
        except IndexError:
            return aliases
    return aliases

def extract_aliases_3(vpn_list):
    """
    Recommended locations:
    - ALIAS COUNTRY     LOCATION   RECOMMENDED
    - ----- ---------------    ------------------------------ -----------
    """
    aliases = []
    for vpn_item in vpn_list[3:]:
        try:
            count = 0
            alias = ''
            for txt in vpn_item.split():
                if count == 0 and re.match("^-.*$", txt):
                    continue
                else:
                    if not re.match("^\(.*\)$", txt):
                      alias = txt if count == 0 else alias + ' ' + txt
                count = count +1
            if alias != '':
              aliases.append(alias)
            # alias = vpn_item.split()[0]
            # aliases.append(alias)
        except IndexError:
            continue
            # return aliases
    # print('aliases:', aliases)
    return aliases


def random_connect(list_vpn_region = []):
    # activation_check()
    disconnect()
    aliases = []
    if len(list_vpn_region) > 0:
      aliases = list_vpn_region
    else:
      # vpn_list = run_command(VPN_LIST)[0:46]  # we use only US, UK, HK and JP VPN. Fastest ones!
      vpn_list = run_command(VPN_LIST)
      # print_output(vpn_list)
      aliases = extract_aliases(vpn_list)
    random.shuffle(aliases)
    selected_alias = aliases[0]
    connect_alias(selected_alias)  # might raise a ConnectException.

def get_vpn_list():
  vpn_list = run_command(VPN_LIST)
  aliases = extract_aliases(vpn_list)
  return aliases
