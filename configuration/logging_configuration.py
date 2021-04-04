import logging
import sys


class _ExcludeErrorsFilter(logging.Filter):
    def filter(self, record):
        """Only returns log messages with log level below ERROR (numeric value: 40)."""
        return record.levelno < 40


new_config = {
    'version': 1,
    'filters': {
        'exclude_errors': {
            '()': _ExcludeErrorsFilter
        }
    },
    'formatters': {
        # Modify log message format here or replace with your custom formatter class
        'basic_formatter': {
            'format': '%(asctime)s - [%(levelname)s] %(name)s [%(threadName)s %(thread)d] [%(module)s.%('
                      'funcName)s:%(lineno)d]: %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S'
        }
    },
    'handlers': {
        'console_stderr': {
            # Sends log messages with log level ERROR or higher to stderr
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'formatter': 'basic_formatter',
            'stream': sys.stderr
        },
        'console_stdout': {
            # Sends log messages with log level lower than ERROR to stdout
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'basic_formatter',
            'filters': ['exclude_errors'],
            'stream': sys.stdout
        }
    },
    'root': {
        # In general, this should be kept at 'NOTSET'.
        # Otherwise it would interfere with the log levels set for each handler.
        'level': 'NOTSET',
        'handlers': ['console_stderr', 'console_stdout']
    }
}
