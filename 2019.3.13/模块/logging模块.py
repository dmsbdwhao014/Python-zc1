import logging
#
# logging.basicConfig(filename='example.log',level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
# logging.debug('this is debug message')
# logging.info(' This is info message')
# logging.error(' This is error message')
# logging.warning(' This is warning message')
# logging.critical(' This is critical message')

# create logger
logger = logging.getLogger('TEST-LOG')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create file handler and set level to warning
fh = logging.FileHandler("access.log")
fh.setLevel(logging.WARNING)
fh1 = logging.FileHandler("access1.log")
fh1.setLevel(logging.WARNING)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter1 = logging.Formatter('%(asctime)s - %(process)d - %(thread)s - %(message)s')

# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)
fh1.setFormatter(formatter1)

# add ch and fh to logger
logger.addHandler(ch)
logger.addHandler(fh)
logger.addHandler(fh1)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')