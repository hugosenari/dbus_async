class Service():
    def __init__(self, name, path="/", interface=None):
        self.name = name
        self.path = path
        self.interface = interface or name

    def get(self, attr_name, getter, output):
        pass
    
    def set(self, attr_name, setter, input):
        pass
    
    def method(self, name, method, input=None, output=None):
        pass
    
    def signal(self, name, output='s'):
        pass
    
    def export(self, bus):
        pass
