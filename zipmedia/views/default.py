"""
default
"""

import colander
import deform.widget
import logging
from pyramid_debugtoolbar import toolbar

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from zipmedia import _
from .. import models

LOG = logging.getLogger(__name__)

DB_ERR_MSG = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

# @view_config(route_name='home', renderer='../templates/mytemplate.xhtml')
# def my_view(request):
#     """ default view """
#     try:
#         query = request.dbsession.query(models.MyModel)
#         one = query.filter(models.MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(DB_ERR_MSG, content_type='text/plain', status=500)
#     return {'title': 'Index',
#             'one': one,
#             'project': 'ZipMedia'
#            }


@view_config(route_name='tal', renderer='')
def xhtml_view(request):
    """
    This is a default renderer for tal documents
    """
    try:
        template = request.matchdict['template']
        LOG.debug('The template is: %s', template)
        request.override_renderer = '../xhtml/' + template
        request.response.content_type = "application/xhtml+xml"

        toolbar.toolbar_html_template = """\
<link rel="stylesheet" type="text/css" href="%(css_path)s" />

<div id="pDebug">
    <div %(button_style)s id="pDebugToolbarHandle">
        <a title="Show Toolbar" id="pShowToolBarButton"
           href="%(toolbar_url)s" target="pDebugToolbar">&#171;</a>
    </div>
</div>
"""

        query = request.dbsession.query(models.MyModel)
        one = query.filter(models.MyModel.name == 'one').first()
    except DBAPIError:
        return Response(DB_ERR_MSG, content_type='text/plain', status=500)
    return {'title': _('Index'),
            'one': one,
            'project': 'ZipMedia',
            'id': template,
           }

@view_config(route_name='locale')
def set_locale_cookie(request):
    """ set_locale_cookie """
    language = request.matchdict['language']
    if language:
        response = Response()
        response.set_cookie('_LOCALE_',
                            value=language,
                            max_age=31536000)  # max_age = year
    return HTTPFound(location=(request.environ['HTTP_REFERER'] if 'HTTP_REFERER'
                               in request.environ
                               else request.route_url('search')),
                     headers=response.headers)
