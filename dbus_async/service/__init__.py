class Service():
    def __init__(self, name, path=None, interface=None):
        self.name = name
        self.path = path or '/'
        self.interface = interface or name
        self.attrs = {}
        self.methods = {}
        self.signals = {}

    def get(self, attr_name, getter, outs):
        attr = self.attrs.get(attr_name, {})
        attr['getter'] = getter
        attr['outs'] = outs
        self.attrs[attr_name] = attr
    
    def set(self, attr_name, setter, ins):
        attr = self.attrs.get(attr_name, {})
        attr['setter'] = setter
        attr['ins'] = ins
        self.attrs[attr_name] = attr
    
    def method(self, name, method, ins=None, outs=None):
        self.methods[name] = {
            'method': method,
            'ins': ins,
            'outs': outs
        }
    
    def signal(self, name, outs):
        self.signals[name] = {
            'outs': outs
        }
    
    def export(self, bus, loop=None):
        print(bus.connect(loop))
