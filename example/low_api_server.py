import asyncio
from dbus_async.server import DefMethod, DefSignal, SessionBus

@asyncio.coroutine
def dbus_hello_server(bus):
    # create message
    helloWorld = DefMethod("HelloWorld",
                           path="/remote/object/path",
                           iface="com.example.Sample",
                           params="s",
                           result="s",
                           bus=bus)

    # wait call
    call = yield from helloWorld.wait()
    
    #do something with params
    print(call.params)
    
    #respond
    response = "Hello World {}".format(call.params[0])
    call.respond(response)

@asyncio.coroutine
def dbus_hello_server_signal(bus):
    # define signal
    signal = DefSignal(
        "HelloWorlded",
        path="/remote/object/path",
        iface="com.example.Sample",
        result="s",
        bus=bus
    )
    
    # emit signal
    signal.emit("voodoo boo boo")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    bus = SessinoBus()
    coro = bus.start(dbus_hello_server, dbus_hello_server_signal)
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
