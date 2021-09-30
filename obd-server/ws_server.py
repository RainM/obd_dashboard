import asyncio
import websockets

import obd_gateway

CLIENTS = set()
num_messages_sent = 0

async def broadcast(q):
    global num_messages_sent
    while True:
        msg = await q.get()
        num_messages_sent += 1
        for ws in CLIENTS:
            await ws.send(msg)
        q.task_done()

async def my_generator(ws, path):
    CLIENTS.add(ws)
    try:
        async for message in ws:
            await ws.send(message)
    except websockets.exceptions.ConnectionClosedError:
        pass
    finally:
        CLIENTS.remove(ws)

async def statistics(timeout):
    global CLIENTS
    while True:
        global num_messages_sent
        await asyncio.sleep(timeout)
        print("Sent " + str(num_messages_sent) + " messages to " + str(len(CLIENTS)) + " clients")
        num_messages_sent = 0

async def main():
    async with websockets.serve(my_generator, "0.0.0.0", 8083):
        def put_to_eventloop_(msg, loop, q):
            loop.call_soon_threadsafe(q.put_nowait, msg)
        Q = asyncio.Queue()
        loop = asyncio.get_running_loop()
        put_to_eventloop = lambda x: put_to_eventloop_(x, loop, Q)

        asyncio.create_task(broadcast(Q))
        asyncio.create_task(statistics(10))
        
        gw = obd_gateway.ObdGateway('/dev/pts/3')
        gw.subscribe_for(obd_gateway.ENGINE_RPM, put_to_eventloop)
        await loop.run_in_executor(None, gw.start)
        print("Started!")
        await asyncio.Future()

asyncio.run(main())


