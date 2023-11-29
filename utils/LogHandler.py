import logging
from logging.handlers import TimedRotatingFileHandler

class LogHandler:
    @staticmethod
    def getLog():
        handler = TimedRotatingFileHandler('../flask.log',
                                           when='D',
                                           interval=1,
                                           backupCount=15,
                                           encoding="UTF-8",
                                           delay=False,
                                           utc=True)
        formatter = logging.Formatter('%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s')
        handler.setFormatter(formatter)
        return handler

