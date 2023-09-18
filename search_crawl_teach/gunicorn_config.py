import multiprocessing

bind = "0.0.0.0:8000"  # Адрес и порт для прослушивания
workers = multiprocessing.cpu_count() * 2 + 1  # Количество рабочих процессов
worker_class = "gthread"  # Используемый рабочий класс (gthread для поддержки асинхронности)
threads = 4  # Количество потоков для каждого рабочего процесса
timeout = 120  # Таймаут для запросов в секунда