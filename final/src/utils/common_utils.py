import datetime
import queue


log_queue = queue.Queue()


def log_writer(log_file, server_running):
    while server_running.is_set():
        try:
            log_message = log_queue.get(timeout=1)  # Agrego timeout para prevenir un bloqueo indefinido
            if log_message is None:
                break
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_file, 'a') as f:
                f.write(f'{timestamp} - {log_message}\n')
        except queue.Empty:
            pass

def get_table_rows(recitals):
    table_header = "Id | Artista | Fecha | Lugar | Link\n"
    table_rows = []
    for recital in recitals:
        date = recital.date.strftime('%Y-%m-%d') if recital.date else ''
        row = f"{recital.id} | {recital.artist} | {date} | {recital.venue} | {recital.link}\n"
        table_rows.append(row)

    table = table_header + ''.join(table_rows)
    return table