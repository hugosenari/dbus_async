from dbus_async import Session, Service


def service(loop):
    service = Service('hugosenari.dbus_sync.example')
    
    
    attr_val = 'hello world'
    def getter():
        return attr_val 
    service.get('attribute_name', getter, 's')

    
    def setter(val):
        attr_val = val
        print(val)
    service.set('attribute_name', setter, 's')

    
    def method(p1):
        print('method called with ' + p1)
        return 'hello world'
    service.method('method_name', method, ins='s', outs='s')

    
    service.signal('signal_name', 's')


    bus = Session(loop)
    service.export(bus)


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    service(loop)
    try:
        loop.run_forever()
    finally:
        loop.close()
