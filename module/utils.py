import logging

def basic_logging_configure():
    logging.basicConfig(filename='logs/etl.log',
                        filemode='a',
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)