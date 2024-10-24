import logging


# class MyFilter(logging.Filter):
# 	def filter(self, record):
# 		return not record.getMessage().__contains__('SomeString we want to exclude from logging')


class ColorCodes:

	green = "\x1b[1;32m"
	yellow = "\x1b[33;20m"
	red = "\x1b[31;20m"
	bold_red = "\x1b[31;1m"
	blue = "\x1b[1;34m"
	light_blue = "\x1b[1;36m"
	purple = "\x1b[1;35m"
	reset = "\x1b[0m"


class ConsoleFormatter(logging.Formatter):
	reset = "\x1b[0m"
	# format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
	# format = "%(levelname)s: %(name)s: %(message)s (%(filename)s:%(lineno)d)"
	format = "%(levelname)s: %(name)s: %(message)s"

	FORMATS = {
		logging.DEBUG: ColorCodes.light_blue + format + reset,
		logging.INFO: ColorCodes.green + format + reset,
		logging.WARNING: ColorCodes.yellow + format + reset,
		logging.ERROR: ColorCodes.red + format + reset,
		logging.CRITICAL: ColorCodes.bold_red + format + reset
	}

	def format(self, record):
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)


class FileFormatter(logging.Formatter):
	format = "'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"


def getMyLogger(name):
	logger = logging.getLogger(name)
	logger.propagate = False	# do not propagate po parent logger's handlers

	logger.setLevel(logging.DEBUG)
	# logger.addFilter(MyFilter())

	# console logging
	stream_handler = logging.StreamHandler()
	stream_handler.setFormatter(ConsoleFormatter())
	logger.addHandler(stream_handler)

	# file logging
	file_handler = logging.FileHandler('./replicator.log')
	file_handler.setFormatter(logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s'))
	logger.addHandler(file_handler)

	return logger
