"""
utils
"""

import os
import logging
import zipstream
import zipfile

def create_zipstream(path):
    """
    return zipstream
    if there is a directory named '~~~' inside the path, then
    the directory is ready to be compressed.
    otherwise an exeption is throw.
    """

    the_zs = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_STORED)

    for root, dirs, files in os.walk(path):
        logging.debug("the root is %s", root)
        logging.debug("the dir is %s", dirs)
        if root == path and '~~~' not in dirs:
            logging.debug("~~~ not in dirs")
            raise Exception('~~~ not in dirs')
        for the_file in files:
            filename = os.path.join(root, the_file)
            arcname = filename
            if root.startswith(path):
                arcname = filename[len(path):]
            logging.debug("the filename is %s and arcname is %s", filename, arcname)
            the_zs.write(filename=filename, arcname=arcname)
    return the_zs

def status_zipstream(path):
    """
    return a tuple with status (exists, ready)
    """

    exists, ready = (False, False)
    exists = exists_path(path)
    if exists:
        logging.debug("the path exists")
        # exists
        ready = ready_to_zip(path)
        if ready:
            logging.debug("the path is ready to zip")
        else:
            logging.debug("the path is ***NOT*** ready to zip")
    else:
        logging.debug("the path ***DON'T*** exist")

    return exists, ready

def status_zipfile(path):
    """
    return a tuple with status (exists, ready) for a given zipfile
    """

    exists, ready = (False, False)
    exists = exists_file(path)
    if exists:
        logging.debug("the path exists")
        # exists
        ready = zipfile.is_zipfile(path)
        ready = True
        if ready:
            logging.debug("the file is zip")
        else:
            logging.debug("the path is ***NOT*** zip")
    else:
        logging.debug("the path ***DON'T*** exist")

    return exists, ready

def exists_path(path):
    """
    return True if path exists
    """

    return os.path.isdir(path)

def exists_file(path):
    """
    return True if path exists
    """

    return os.path.isfile(path)

def ready_to_zip(path):
    """
    return True if directory is ready to be zipped.
    """

    ready = False

    for root, dirs, _ in os.walk(path, topdown=False):
        logging.debug("the root is %s", root)
        logging.debug("the dir is %s", dirs)
        if root == path and '~~~' in dirs:
            ready = True

    return ready


# For Emacs:
# Local Variables:
# mode: python
# coding: utf-8
# End:
