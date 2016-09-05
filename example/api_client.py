from dbus_async import ProxyObject

  
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    bus = SessinoBus()
    obj = bus.Object("com.example.Sample",
               path="/remote/object/path",
               iface="com.example.Sample")
    co = obj.HelloWorld("Anon")
    ro = obj.prop
    tine = obj.HelloWorlded
    