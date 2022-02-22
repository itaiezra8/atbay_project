from core.utils.logger import Logger
from postgresql.utils.consts import SERVICE_NAME

postgresql_logger = Logger(SERVICE_NAME)
logger = postgresql_logger.get_logger()
