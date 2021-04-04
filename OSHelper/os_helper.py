"""
This module includes methods for handling OS related tasks such as: saving and reading files, getting information on a
file, validating a file path.
"""

import logging
import pathlib
import json
import functools
import platform
import datetime

logger = logging.getLogger(__name__)
logger.debug("Logging in {} configured.".format(__name__))


class OSHelper():

    def __init__(self):
        logger.debug('An instance of the class {} created.'.format(__class__.__name__))

    def __repr__(self):
        return 'OSHelper instance'

    def path_constructor(self, *path_elements, path_null=''):
        """
        Parameters
        ----------
        path_elements : str or pathlib.PosixPath or pathlib.WindowsPath
            Directories and file that constitute the output path. They are read in the order as they appear in the
            function call left to right.
        path_null : str
            This is a value representing an empty path.

        Returns
        ----------
        potential_path : pathlib.PosixPath or pathlib.WindowsPath
            This path is not validated existence-wise - may or may not exist.
        """

        # Windows pitfall: may change this to WindowsPath on Windows-based machines.
        # The Windows option has not been tested.
        os_platform = platform.system()
        if os_platform == 'Linux':
            path_blocks = [pathlib.PosixPath(path_null)]
        elif os_platform == 'Windows':
            path_blocks = [pathlib.WindowsPath(path_null)]
        else:
            raise NotImplemented('The path handling for the OS {} is not supported.'.format(os_platform))

        path_blocks.extend(list(path_elements))

        potential_path = functools.reduce(lambda x, y: x.joinpath(y), path_blocks)
        return potential_path

    def validate_path(self, path, acceptable_types=(pathlib.PosixPath, pathlib.WindowsPath)):
        """
        Parameters
        ----------
        acceptable_types : tuple
            Path types that are accepted (subset of pathlib types)
        path : Object
            A potential path. Any object can be passed here.

        Returns
        ----------
        : boolean
            Whether or not the `path` may be considered a valid `pathlib` object.

        Raises
        ----------
        TypeError:
            The `path` provided is not of the `acceptable_types`.
        FileNotFoundError:
            The `path` is of one of `acceptable_types` but does not point ot anything in the file system.
        """

        if not isinstance(path, acceptable_types):
            raise TypeError('Path {} is of type {}. It should be one of these types: {}.'.format(path
                                                                                                 , type(path)
                                                                                                 , acceptable_types))

        # check if there is really such a location:
        if path.exists():
            return True
        else:
            raise FileNotFoundError('{} does not exist.'.format(str(path.absolute())))

    def read_json_file(self, **kwargs):
        """
        Parameters
        ----------
        json_file_path : str or pathlib.PosixPath or pathlib.WindowsPath
            If the path provided is a string a path is constructed and then validated. If the path provided is an object
            from the `pathlib` library only the validation method is called.
        directory : str or pathlib.PosixPath or pathlib.WindowsPath
            If the path provided is a string a path is constructed and then validated. If the path provided is an object
            from the `pathlib` library only the validation method is called.
        file_name : str or pathlib.PosixPath or pathlib.WindowsPath
            If the path provided is a string a path is constructed and then validated. If the path provided is an object
            from the `pathlib` library only the validation method is called.

        Returns
        ---------
        contents : dict
            Contents of a JSON file.

        Raises
        ----------

        """

        json_file_path = kwargs.get('json_file_path')
        directory = kwargs.get('directory')
        file_name = kwargs.get('file_name')

        if json_file_path:
            if isinstance(json_file_path, str):
                potential_path = self.path_constructor(json_file_path)
            else:
                potential_path = json_file_path
        elif directory and file_name:
            potential_path = self.path_constructor(directory, file_name)
        else:
            message = """The read_json_file method of {} requires either: 
                json_file_path argument or 
                directory and file_name arguments'
            """.format(self)
            raise TypeError(message)

        if self.validate_path(potential_path):
            with open(potential_path, 'r') as json_file:
                try:
                    contents = json.load(json_file)
                except json.JSONDecodeError as e:
                    raise ValueError('Error: {}.\nFile: {}'.format(e, str(potential_path.absolute())))

        return contents

    def get_file_modification_time(self, file_path):
        """
        Get file's modification time and return a datetime object.

        Parameters
        ----------
        file_path : pathlib.PosixPath or pathlib.WindowsPath
            Path's not validated.

        Returns
        ----------
        mod_datetime : datetime.datetime
        """
        if self.validate_path(file_path):
            file_info = file_path.stat()
            mod_datetime = datetime.datetime.fromtimestamp(file_info.st_mtime)
        else:
            raise TypeError("This type of path is not supported.")

        return mod_datetime

    def get_current_time(self):
        """
        Return current time as a datetime object.

        Returns
        ----------
        current_datetime : datetime.datetime
        """

        return datetime.datetime.today()
