import logging
import logging.config
from pathlib import Path

log_root_path = Path(__file__).resolve().parents[0]
logging.config.fileConfig(log_root_path / 'log.conf',
                          defaults={ 'logfile' : log_root_path / 'logs.log' })

sys_logger = logging.getLogger('systemLogger')
request_logger = logging.getLogger('requestLogger')
# defaults={ 'logfilename' : getSomeName() }