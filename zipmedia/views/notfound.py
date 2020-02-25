from pyramid.view import notfound_view_config


@notfound_view_config(renderer='../xhtml/404.xhtml')
def notfound_view(request):
    """ not found """
    request.response.status = 404
    return {'title': '404 Not Found'}
