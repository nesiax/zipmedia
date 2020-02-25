"""
Main
"""

import re

from pyramid.config import Configurator
from pyramid.i18n import TranslationStringFactory
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request

# Deform i18n
from deform.renderer import configure_zpt_renderer

_ = TranslationStringFactory('zipmedia')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    # pylint: disable=unused-argument
    with Configurator(settings=settings,
                      ) as config:
        config.include('.models')
        config.include('pyramid_chameleon')
        config.include('.routes')
        config.include('.tweaks')
        #import pdb; pdb.set_trace()
        # Add CSV Renderer
        config.add_renderer('csv', 'zipmedia.renderers.CSVRenderer')
        # Add Zip Renderer
        config.add_renderer('zip', 'zipmedia.renderers.ZipRenderer')
        # Add Translation Service
        config.add_translation_dirs(
            "colander:locale", "deform:locale", 'zipmedia:locale'
        )

        # deform translator
        def translator(term):
            return get_localizer(get_current_request()).translate(term)

        # deform renderer
        configure_zpt_renderer([], translator)


        config.scan(ignore=[re.compile(r"\.flycheck_.*").search])

    return config.make_wsgi_app()
