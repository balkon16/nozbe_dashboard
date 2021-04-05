"""
This module provides a class responsible for communicating with Nozbe's API.
"""
import json
import logging
import requests

from modules.OSHelper.os_helper import OSHelper


class APIHandler:
    """
    This class handles communication between the application and the Nozbe API. The features include but are not
    limited to:
        1. Getting the token.
        2. Authenticating.
        3. Performing a request.
        4. Saving a response as a file.
    """

    os_helper = OSHelper()

    def __init__(self, current_dir, credentials_dir_name, credentials_file_name, supported_entities):
        """
        current_dir : pathlib.PosixPath or pathlib.WindowsPath
            This is the path of the process instantiating an object of the APIHandler class.
        credentials_dir_name : str
            This is the location of secret files with credentials. The credentials directory must be a child of the
            `current_dir`.
        credentials_file_name : str
            The credentials file name (with extension).
        supported_entities : list
            A list (of str) with the names of supported entities.
        """
        try:
            if APIHandler.os_helper.validate_path(current_dir):
                self.current_dir = current_dir
        except TypeError as err1:
            logging.error(f"Couldn't create an instance of class {self.__class__.__name__}: {err1}")
            return
        except FileNotFoundError as err2:
            logging.error(f"Couldn't create an instance of class {self.__class__.__name__}: {err2}")
            return

        self.credentials_dir = self.current_dir / credentials_dir_name
        self.credentials_dict = APIHandler.os_helper.read_json_file(directory=self.credentials_dir
                                                                    , file_name=credentials_file_name)
        self.supported_entities = supported_entities
        logging.debug("Initialized an instance of API Handler class.")

    def __repr__(self):
        return f"Instance of {self.__class__.__name__} class. Location: {str(self.current_dir.absolute())}"

    def __str__(self):
        return f"Instance of {self.__class__.__name__} class. Location: {str(self.current_dir.absolute())}"

    @staticmethod
    def _send_get_request(url, params, payload):
        """
        Send a GET request.

        Parameters
        ----------
        url : str

        params : dict

        payload : dict, str

        Returns
        ----------
        str, None
        """
        try:
            request = requests.get(url=url, params=params, data=payload)
            status_code = request.status_code
            text = request.text
        except requests.ConnectionError as err:
            logging.error(f'Error: {err}. Check the url: {url}.')
            return None

        if status_code == 200:
            logging.debug(f"GET request to {url} successful.")
            return text
        if str(status_code).startswith('5'):
            logging.warning(f'PUT request to {url} unsuccessful. Problem with the server.\nReturn code: {status_code}.')
            return None
        if str(status_code).startswith('4'):
            logging.error(f'PUT request to {url} unsuccessful.\nReturn code: {status_code}.\nMessage: {text}')
            return None
        raise NotImplementedError(f'No handling for error no.: {status_code}.')

    @staticmethod
    def _send_put_request( url, headers, payload):
        """
        Send a PUT request.

        Parameters
        ----------
        url : str

        headers : dict

        payload : dict, None

        Returns
        ----------
        object
        """
        try:
            request = requests.put(url=url, headers=headers, data=payload)
            status_code = request.status_code
            text = request.text
        except requests.ConnectionError as err:
            logging.error(f'Error: {err}. Check the url: {url}.')
            return None

        if status_code == 200:
            logging.debug(f"PUT request to {url} successful.")
        elif str(status_code).startswith('5'):
            logging.warning(f'PUT request to {url} unsuccessful. Problem with the server.\nReturn code: {status_code}.')
        elif str(status_code).startswith('4'):
            logging.error(f'PUT request to {url} unsuccessful.\nReturn code: {status_code}.\nMessage: {text}')
        else:
            raise NotImplementedError(f'No handling for error no.: {status_code}.')

        return None

    def refresh_token(self, url):
        """

        Parameters
        ----------
        url : string
            URL of the endpoint used for refreshing the token.
        """
        logging.info(f'{self}: Refreshing token.')
        self._send_put_request(url=url,
                               headers={'Authorization': self.credentials_dict['access_token']},
                               payload=None)

    def get_entity_data(self, endpoint, entity_type):
        """

        Parameters
        ----------
        endpoint : str
            An endpoint providing data for a given entity type.
        entity_type : str
            Allowed entity types are: task.
        Returns
        -------
        content : list, None
            Returns a list of dictionaries if successful, None otherwise.
        """

        if entity_type not in self.supported_entities:
            raise NotImplementedError(f"Fetching data for type {entity_type} is not implemented.")
        data = 'type={}'.format(entity_type)
        params = {"access_token": self.credentials_dict['access_token']}
        try:
            returned_text = self._send_get_request(url=endpoint, params=params, payload=data)
            try:
                if returned_text:
                    content = json.loads(returned_text)
                    return content
                return None
            except json.decoder.JSONDecodeError as err:
                logging.error(f"Couldn't fetch data for {entity_type} type: {err}")
                return None
        except NotImplementedError as err:
            logging.error(f"Couldn't fetch data for {entity_type} type: {err}")
            return None
