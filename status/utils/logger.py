from core.utils.logger import Logger
from status.utils.consts import SERVICE_NAME

status_logger = Logger(SERVICE_NAME)
logger = status_logger.get_logger()
