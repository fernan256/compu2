import socket, pickle, argparse
import asyncio


async def client(args):
    host = args.host
    port = int(args.port)
    reader, writer = await asyncio.open_connection(
        host, port)

    while True:
        msg1 = input("> ")
        msg1 = pickle.dumps(msg1)
        writer.write(msg1)
        await writer.drain()

        msg2 = await reader.read(1024)
        msg2 = pickle.loads(msg2)

        if pickle.loads(msg1).lower() == "exit":
            print(f"Server: {msg2}")

            writer.close()
            await writer.wait_closed()
            exit()

        if msg2["error"] == "":
            print("OK\n", msg2["output"])
        else:
            print("ERROR\n", msg2["error"])
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-hs", '--host', required=True, help='host del sever')
    parser.add_argument("-p", '--port', required=True, help='Puerto de conexion')
    args = parser.parse_args()
    asyncio.run(client(args))



