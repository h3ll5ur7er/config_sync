from hashlib import md5

HASH_ALGORITHM = md5
DEFAULT_HASH = "00000000000000000000000000000000" 
DISCOVERY_SERVER_PORT = 54321
DISCOVERY_SERVER_BROADCAST_ADDR = "255.255.255.255"
# IP multicasts are in the range of 224.0.0.0 to 239.255.255.255
# DISCOVERY_SERVER_BROADCAST_ADDR = "224.0.0.1"