import logging

class Logger:

    def __init__(self):
        #self.logger = logging.getLogger(__name__)
        # logging.basicConfig(filename='logs.log', level=logging.INFO, encoding='UTF-8')
        self.logger = logging.getLogger('ИнcпeктopLogger')
        self.logger.setLevel(logging.DEBUG)  # Записываем всё

        # Обработчики – это ваш ключ к продвинутому логированию
        file_handler = logging.FileHandler('logs.log', 'a', encoding="UTF-8") # Дописываем в конец файла, а не перезаписываем его
        file_handler.setLevel(logging.INFO)  # Нас интересуют только ошибки

        # Форматируем сообщения
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        file_handler.setFormatter(log_format)

        # Присоедините обработчик к логгеру
        self.logger.addHandler(file_handler)
    


    def log_info(self, info: str):
        self.logger.info(info)
    
    def log_error(self, error: str):
        self.logger.error(error)

