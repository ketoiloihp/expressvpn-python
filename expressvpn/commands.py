import subprocess
# expressvpn connect [ALIAS]

VPN_CONNECT = 'expressvpn connect'
VPN_LIST = 'expressvpn list'
VPN_DISCONNECT = 'expressvpn disconnect'
IS_MAC =  False

# check if expresso is exist
# status <> 0 not exist
status = subprocess.getstatusoutput('command -v expresso')
if [ status[0] == 0 ]:
  VPN_CONNECT = 'expresso connect'
  VPN_LIST = 'expresso locations'
  VPN_DISCONNECT = 'expresso disconnect'
  IS_MAC =  True
