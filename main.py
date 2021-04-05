"""
This the module that serves as an entry point.
"""

# TODO: script for installing and starting Airflow in a container:
#  https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html#running-the-cli-commands
# TODO: prepare a script for running pylint on all .py files in the project

import logging
from logging.config import dictConfig
import os
import sys

from configuration.logging_configuration import new_config
from modules.APIHandler.api_handler import APIHandler
from modules.OSHelper.os_helper import OSHelper

CONFIGURATION_DIR = 'configuration'
CONFIGURATION_FILE = 'app_configuration.json'

dictConfig(new_config)

logger = logging.getLogger()
logger.debug(f"Logging configured in module {__name__}.")


def main():
    """
    The entry point.
    """
    os_helper = OSHelper()
    app_configuration = os_helper.read_json_file(directory=CONFIGURATION_DIR, file_name=CONFIGURATION_FILE)
    nozbe_configuration = app_configuration['nozbe']
    general_configuration = app_configuration['general']
    current_dir_str = os.path.dirname(sys.argv[0])
    current_dir_pathlib = os_helper.construct_path(current_dir_str)
    api_handler = APIHandler(current_dir=current_dir_pathlib,
                             credentials_dir_name=nozbe_configuration['credentials_file']['directory'],
                             credentials_file_name=nozbe_configuration['credentials_file']['file_name'],
                             supported_entities=nozbe_configuration['entities'])
    api_handler.refresh_token(url=nozbe_configuration['endpoints']['refresh_token'])

    for entity_name in nozbe_configuration['entities']:
        logger.info(f"Getting data for {entity_name} entity...")
        content = api_handler.get_entity_data(endpoint=nozbe_configuration['endpoints']['data'],
                                              entity_type=entity_name)
        filename = "{}_{}.json".format(entity_name,
                                       os_helper.get_current_time().strftime(general_configuration['datetime_format']))

        data_dir_pathlib = os_helper.construct_path(current_dir_pathlib, general_configuration['data']['directory'])
        os_helper.write_json_file(data_dir_pathlib, filename, content)


if __name__ == "__main__":
    main()
