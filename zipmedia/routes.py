"""
routes
"""

def includeme(config):
    """ route list """

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('zipfile', 'zipmedia:zipfile', cache_max_age=3600)
    #import pdb;  pdb.set_trace()
    config.override_asset(to_override='zipmedia:zipfile/',
                          override_with=config.registry.settings.get(
                              'zipmedia.path', 'zipfile'))

    # app
    config.add_route('search', '/')
    config.add_route('download', '/download/{zip_id}')
    config.add_route('zipstream', '/zipstream/{zip_id}')
    config.add_route('about', '/about')

    # i18n
    config.add_route('locale', '/locale/{language}')

    # xhtml test
    config.add_route('tal', r"/{template:.+[.]xhtml}")

    # deform
    config.add_static_view('deform_static', 'deform:static/')
