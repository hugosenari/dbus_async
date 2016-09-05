import dbus_async

@asyncio.coroutine
def dbus_hello_client(bus): 
    # create message
    helloWorld = Method("HelloWorld",
                        path="/remote/object/path",
                        iface="com.example.Sample",
                        bus=bus)
    # wait reply
    result = yield from helloWorld("Anon")
    
    #do something with response
    if (result) {
       print(result)
    }

@asyncio.coroutine
def dbus_hello_client_signal(bus):
    # define signal
    signal = Signal(
        "HelloWorlded",
        path="/remote/object/path",
        iface="com.example.Sample"
        bus=bus
    )
    
    # wait signal
    result = yield from signal.wait()
    
    #do something with response
    if (result) {
       print(result)
    }

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    bus = SessinoBus()
    coro = bus.start(dbus_hello_client, dbus_hello_client_signal)
    con = loop.run_until_complete(coro)
    # Stay connected until Ctrl+C is pressed
    print('Connected on {}'.format(bus))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    con.close()
    loop.run_until_complete(con.wait_closed())
    loop.close()