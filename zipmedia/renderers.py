"""
Custom CSV Render
"""

import logging
import csv
import zipmedia.utils as utils
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response

LOG = logging.getLogger(__name__)

try:
    from StringIO import StringIO
    from BytesIO import BytesIO # python 2
except ImportError:
    from io import StringIO, BytesIO # python 3

class CSVRenderer(object):
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        """ Returns a plain CSV-encoded string with content-type
        ``text/csv``. The content-type may be overridden by
        setting ``request.response.content_type``."""

        request = system.get('request')
        if request is not None:
            response = request.response
            ct = response.content_type
            if ct == response.default_content_type:
                response.content_type = 'text/csv'

        fout = StringIO()
        writer = csv.writer(fout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(value.get('header', []))
        writer.writerows(value.get('rows', []))

        return fout.getvalue()

class ZipRenderer(object):
    """ zip renderer """
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        """ Returns a zip file with content-type
        ``application/zip``. The content-type may be overridden by
        setting ``request.response.content_type``."""

        request = system.get('request')
        if request is not None:

            fout = BytesIO()

            try:
                the_zs = utils.create_zipstream(value.get('path', []))
                for chunk in the_zs:
                    fout.write(chunk)

                response = request.response
                ct = response.content_type
                if ct == response.default_content_type:
                    response.content_type = 'application/zip'

            except Exception as exc:
                #import pdb; pdb.set_trace()
                LOG.debug('In tweens')
                msg = exc.args[0] if exc.args else ""
                response =  Response('Failed validation: %s' % msg)
                response.status_int = 500
                return response

            return fout.getvalue()

# For Emacs:
# Local Variables:
# mode: python
# coding: utf-8
# End:
