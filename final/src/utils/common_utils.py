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