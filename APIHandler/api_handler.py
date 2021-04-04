"""
This class handles communication between the application and the Nozbe API. The features include but are not limited to:
1. Getting the token.
2. Authenticating.
3. Performing a request.
4. Saving a response as a file.
"""

import requests
import logging
import json

from OSHelper.os_helper import OSHelper



class APIHandler:
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
            logging.error("Couldn't create an instance of class {}: {}".format(self.__class__.__name__, err1))
            return
        except FileNotFoundError as err2:
            logging.error("Couldn't create an instance of class {}: {}".format(self.__class__.__name__, err2))
            return

        self.credentials_dir = self.current_dir / credentials_dir_name
        self.credentials_dict = APIHandler.os_helper.read_json_file(directory=self.credentials_dir
                                                                    , file_name=credentials_file_name)
        self.supported_entities = supported_entities
        logging.debug("Initialized an instance of API Handler class.")

    def __repr__(self):
        return "Instance of {} class. Location: {}".format(self.__class__.__name__, str(self.current_dir.absolute()))

    def __str__(self):
        return "Instance of {} class. Location: {}".format(self.__class__.__name__, str(self.current_dir.absolute()))

    def _send_get_request(self, url, params, payload):
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
            r = requests.get(url=url, params=params, data=payload)
            status_code = r.status_code
            text = r.text
        except requests.ConnectionError as e:
            logging.error('Error: {}. Check the url: {}.'.format(e, url))
            return None

        if status_code == 200:
            logging.debug("GET request to {} successful.".format(url))
            return text
        elif str(status_code).startswith('5'):
            logging.warning('PUT request to {} unsuccessful. Problem with the server.\nReturn code: {}.' \
                            .format(url, status_code))
            return None
        elif str(status_code).startswith('4'):
            logging.error('PUT request to {} unsuccessful.\nReturn code: {}.\nMessage: {}' \
                          .format(url, status_code, text))
            return None
        else:
            raise NotImplementedError('No handling for error no.: {}.'.format(status_code))

    def _send_put_request(self, url, headers, payload):
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
            r = requests.put(url=url, headers=headers, data=payload)
            status_code = r.status_code
            text = r.text
        except requests.ConnectionError as e:
            logging.error('Error: {}. Check the url: {}.'.format(e, url))
            return

        if status_code == 200:
            logging.debug("PUT request to {} successful.".format(url))
        elif str(status_code).startswith('5'):
            logging.warning('PUT request to {} unsuccessful. Problem with the server.\nReturn code: {}.' \
                            .format(url, status_code))
        elif str(status_code).startswith('4'):
            logging.error('PUT request to {} unsuccessful.\nReturn code: {}.\nMessage: {}' \
                          .format(url, status_code, text))
        else:
            raise NotImplementedError('No handling for error no.: {}.'.format(status_code))

        return None

    def refresh_token(self, url):
        logging.info('{}: Refreshing token.'.format(self))
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
            raise NotImplementedError("Fetching data for type {} is not implemented.".format(entity_type))
        data = 'type={}'.format(entity_type)
        params = {"access_token": self.credentials_dict['access_token']}
        try:
            returned_text = self._send_get_request(url=endpoint, params=params, payload=data)
            if returned_text:
                content = json.loads(returned_text)
                return content
            else:
                return None
        except BaseException as err:
            logging.error("Couldn't fetch data for {} type: {}".format(entity_type, err))
            return None
