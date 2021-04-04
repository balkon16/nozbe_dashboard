import logging
from logging.config import dictConfig
import os
import sys

from configuration.logging_configuration import new_config
from APIHandler.api_handler import APIHandler
from OSHelper.os_helper import OSHelper

CONFIGURATION_DIR = 'configuration'
CONFIGURATION_FILE = 'app_configuration.json'

dictConfig(new_config)

logger = logging.getLogger()
logger.debug("Logging configured in module {}.".format(__name__))


def main():
    os_helper = OSHelper()
    app_configuration = os_helper.read_json_file(directory=CONFIGURATION_DIR, file_name=CONFIGURATION_FILE)
    nozbe_configuration = app_configuration['nozbe']
    current_dir_str = os.path.dirname(sys.argv[0])
    current_dir_pathlib = os_helper.path_constructor(current_dir_str)
    api_handler = APIHandler(current_dir=current_dir_pathlib,
                             credentials_dir_name=nozbe_configuration['credentials_file']['directory'],
                             credentials_file_name=nozbe_configuration['credentials_file']['file_name'])
    api_handler.refresh_token(url=nozbe_configuration['endpoints']['refresh_token'])
    tasks = api_handler.get_entity_data(endpoint=nozbe_configuration['endpoints']['data'], entity_type='task')
    print(tasks)

if __name__ == "__main__":
    main()
