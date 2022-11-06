import argparse, pickle
import subprocess as sp
import asyncio


def remote_shell(msg_client):
    command = sp.Popen(msg_client, stdout=sp.PIPE, stderr=sp.PIPE, shell=True, universal_newlines=True, bufsize= 10000)
    output, error = command.communicate()

    return {"output": output, "error": error}


async def handle_echo(reader, writer):
    for t in asyncio.all_tasks():
        print(f"Tarea: {t}")

    addr = writer.get_extra_info('peername')

    print(f"Cliente {addr} conectado.")

    while True:
        msg_client = await reader.read(1024)
        msg_client = pickle.loads(msg_client)

        if msg_client == "exit":
            print(f"Client {addr} saliendo.")
            writer.write(pickle.dumps("By by"))
            await writer.drain()
            writer.close()
            break
        else:
            msg_client_dic = remote_shell(msg_client)
            msg_client_dic = pickle.dumps(msg_client_dic)
            writer.write(msg_client_dic)


        for t in asyncio.all_tasks():
            print(f"Cerrando Tarea: {t}")


async def main(args):
    port = args.p
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', port)

    addr = server.sockets[0].getsockname()
    #print(f'Serving on {addr} {asyncio.current_task()}')

    async with server:
        print(f"Tareas:\n{asyncio.all_tasks()}")
        await server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, required=True, help="Puerto")
    args = parser.parse_args()
    asyncio.run(main(args))

