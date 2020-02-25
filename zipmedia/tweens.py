""" tweens """

import time
#import logging

#from pyramid.settings import asbool

from tidylib import tidy_document

from .tweaks import LOG

#LOG = logging.getLogger(__name__)

def timing_tween_factory(handler, registry):
    """ timming """
    # pylint: disable=unused-argument
    LOG.debug('In tweens')
    # if asbool(registry.settings.get('do_timing')):
    #     # if timing support is enabled, return a wrapper
    def timing_tween(request):
        """ timming """
        start = time.time()
        response = None
        try:
            response = handler(request)
        finally:
            end = time.time()
            # LOG.debug('%s', type(response))
            #import pdb;  pdb.set_trace()
            if (response is not None and response.has_body and
                (response.content_type in ['text/html',
                                           'application/xhtml+xml'
                                           'application/xml',
                                           ]
                 ) and
                (response.status_code in [200, 404])
                ):

                #LOG.debug('%s', response.body)
                # LOG.debug('the status "%s"', response.status_code)
                # LOG.debug('the status "%s"', type(response.status_code))
                # LOG.debug('the content_type %s', type(response.content_type))

                # if (response.status_code == 200 and
                #     response.content_type == 'text/html'):
                if (response.headers.get('do_tidy', '') == 'true' or
                    request.registry.settings.get('do_tidy') == 'true'):
                    LOG.debug('***modificando ***')

                    document, errors = tidy_document(
                        response.body,
                        options={
                            'indent': 'auto',
                            'doctype' : 'html5',
                            'output-xhtml' : 1,
                            'indent-spaces': 2,
                            'quiet' : 1,
                            'wrap': 0,
                            'tidy-mark' : 1,
                            'vertical-space' : 1,
                            'wrap-attributes' : 0,
                            'indent-cdata' : 1,
                            'indent-attributes' : 1,
                            'break-before-br' : 1,
                            'preserve-entities' : 1,
                            'drop-empty-elements' : 0,
                        })
                    LOG.debug('Original: "%s"', response.body)
                    LOG.debug('Errors: "%s"', errors)

                    if response.headers.get('do_tidy', '') == 'true':
                        del request.response.headers['do_tidy']

                    response.body = document

                # Always print request time
                LOG.debug('The request took %s seconds', (end - start))

        return response
    return timing_tween
    # # if timing support is not enabled, return the original
    # # handler
    # return handler
