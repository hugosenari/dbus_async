from dbus_async import Session, Object


def client(loop):
    bus = Session(loop)
    obj = Object(bus, 'hugosenari.dbus_sync.example')

    result = obj.attribute_name
    print(result)
    
    obj.attribute_name = 'hello weird'
    result = obj.attribute_name
    print(result)

    result = obj.method_name('hello weird')
    print(result)

    def on_receive(param):
        print(param)        
    obj.signal_name = on_receive


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    client(loop)
    try:
        loop.run_forever()
    finally:
        loop.close()
