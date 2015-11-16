from os import environ, path, walk
import asyncio as aio
from socket import AF_INET, AF_INET6

SYSTEM_ENV = "DBUS_SYSTEM_BUS_ADDRESS"
SYSTEM_DEFAULT = 'unix:path=/var/run/dbus/system_bus_socket'
SESSION_ENV = "DBUS_SESSION_BUS_ADDRESS"
USER_DIR_CFG = '~/.dbus/session-bus'


class Bus():
    def __init__(self, loop, addr):
        self.loop = loop
        self.addrs = [v for v in self._addr_info(addr)] 
        
    def _addr_info(self, addr):
        addrs = addr.split(';')
        for address in addrs:
            con_type, params = address.split(':')
            info = {'type': con_type}
            for param in params.split(','):
                k,v = param.split('=')
                info[k] = v 
            yield info
            
    def connect(self, loop=None):
        loop = loop or self.loop
        for addr in self.addrs:
            if addr['type'] == 'unix':
                to = addr.get('path')
                to = to or addr.get('tmpdir')
                to = to or addr.get('abstract')
                return aio.open_unix_connection(to, loop=loop)
            elif addr['type'] == 'launchd':
                env = addr.get('env')
                to = environ.get(env, None)
                return aio.open_unix_connection(to, loop=loop)
            elif addr['tcp'] == 'launchd':
                host = addr.get('host', '127.0.0.1')
                bind = addr.get('bind', None)
                port = addr.get('port', None)
                family = addr.get('family', None)
                return aio.open_connection(
                    host=host,
                    port=port,
                    ssl= True if port == '443' else None,
                    family=AF_INET6 if family == 'ipv6' else AF_INET,
                    local_addr=bind
                )
        raise Exception('UNKNOWN ADDRESS TYPE')
            
    
class System(Bus):
    def __init__(self, loop, addr=None):
        addr = addr or environ.get(SYSTEM_ENV, SYSTEM_DEFAULT)
        Bus.__init__(self, loop, addr)


class Session(Bus):
    def __init__(self, loop, addr=None):
        addr = addr or environ.get(SESSION_ENV, None)
        addr = addr or self._get_adrr_from_file()
        Bus.__init__(self, loop, addr) 

    def _get_adrr_from_file(self, userdir=USER_DIR_CFG):
        user_dir = path.expanduser(userdir)
        addr = None
        if path.exists(user_dir):
            if path.isdir(user_dir):
                addr = self._walk_dir_looking_for_addr(user_dir)
            else:
                addr = self._look_for_address(user_dir)
            if addr:
                return addr
        raise Exception('SESSION ADDRESS NOT FOUND')

    def _look_for_address(self, file_name):
        with open(file_name) as bus_info:
            for line in bus_info:
                if line.startswith(SESSION_ENV):
                    return line.replace(SESSION_ENV + '=', '')
                
    def _walk_dir_looking_for_addr(self, dir_name):
        for dirname, dirnames, filenames in walk(dir_name):
            for filename in filenames:
                user_file = path.join(dirname, filename)
                addr = self._look_for_address(user_file)
                if addr:
                    return addr
