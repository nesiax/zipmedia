"""
tweakes
"""

import logging
from pyramid_chameleon import zpt

print("logger (fut)sera: " + __name__)

LOG = logging.getLogger(__name__)

def includeme(config):
    """ tweaks """

    config.add_renderer('.xhtml', zpt.renderer_factory)
    config.add_tween('.tweens.timing_tween_factory')
