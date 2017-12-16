#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals

import logging
import os
import sys

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse

import mainchecker

mainchecker.check_for_main()

file_handler = logging.FileHandler(filename='download_logs.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - %(levelname)s : %(message)s',
    handlers=handlers
)

logger = logging.getLogger(__name__)


def download_file(url, dest=None):
    try:
        """ 
        Download and save a file specified by url to dest directory,
        """
        u = urllib2.urlopen(url)

        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
        filename = os.path.basename(path)
        if not dest is None:
            filename = dest
        else:
            if not filename:
                filename = 'downloaded.file'
            if dest:
                filename = os.path.join(dest, filename)

        with open(filename, 'wb') as f:
            meta = u.info()
            meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
            meta_length = meta_func("Content-Length")
            file_size = None
            if meta_length:
                file_size = int(meta_length[0])
            logging.info("Downloading: {0} Bytes: {1}".format(url, file_size))

            if file_size is None:
                logging.warning('The file has no bytes, retrying download.')
                raise ValueError('The file did not read.')

            file_size_dl = 0
            if file_size > (1024 ** 2) * 100:
                block_sz = int(file_size / 1000)
            elif file_size < (1024 ** 2) * 100 and file_size > (1024 ** 3):
                block_sz = int(file_size / 100)
            elif file_size < (1024 ** 2) and file_size < (1024 ** 1) * 500:
                block_sz = int(file_size / 2)
            else:
                block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += int(len(buffer))
                f.write(buffer)
                status = "{b} bytes, {kb} kilobytes, {mb} megabytes".format(b=str(file_size_dl), kb=str(int(round(
                    file_size_dl / 1024, 0))), mb=str(int(round(file_size_dl / (1024 ** 2), 0))))
                if file_size:
                    status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
                status += chr(13)
                logging.info(status)
            logger.info('Downloaded file {}'.format(str(filename)))
        return filename
    except Exception:
        raise
