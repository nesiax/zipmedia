"""
default
"""

import logging

import colander
import deform.widget

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from pyramid.i18n import get_locale_name
from pyramid.settings import aslist

from zipmedia import _
from zipmedia import utils

LOG = logging.getLogger(__name__)

class Zip:
    """ Zip """

    def __init__(self, request):
        """ init """
        self.request = request
        self.project = "ZipMedia"
        self.zipstream = request.registry.settings.get('zipstream') == 'true'

        #import pdb;  pdb.set_trace()

        self.langs = aslist(
            request.registry.settings.get('available_languages')
        )

        #self.trans = request.localizer.translate

    @view_config(route_name='about',
                 renderer='../xhtml/about.xhtml')
    def about(self):
        """
        About
        """

        # if self.request.registry.settings.get('do_tidy') == 'yes':
        #     self.request.response.headers['do_tidy'] = 'yes'

        return {
            'title': _("About"),
        }

    @view_config(route_name='search',
                 renderer='../xhtml/search.xhtml')
    def search(self):
        """ search """

        locale_name = get_locale_name(self.request)
        LOG.debug('Locale: %s', locale_name)
        # LOG.debug('Download: %s', self.trans(_("Download")))

        #import pdb;  pdb.set_trace()

        class SearchSchema(colander.Schema):
            """ form schema """
            zip_id = colander.SchemaNode(
                colander.String(),
                validator=colander.Length(max=100),
                widget=deform.widget.TextInputWidget(),
                title=_("Identification"),
                name="zip_id",
                description=_("Please type your ID"),
            )

            _LOCALE_ = colander.SchemaNode(
                colander.String(),
                widget=deform.widget.HiddenWidget(),
                default=locale_name,
            )

        def search_form():
            """ return zip id form """
            schema = SearchSchema()
            button_label = deform.Button("submit", _("Submit"))
            form = deform.Form(schema,
                               buttons=[button_label],
                               method="post",
                              )
            return form

        form = search_form()
        reqts = form.get_widget_resources()
        # form_rendered = ""

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
                url = self.request.route_url('download',
                                             zip_id=appstruct['zip_id'])
                return HTTPFound(url)
            except deform.ValidationFailure as exc:
                # Form is NOT valid
                form_rendered = exc.render()
        else:
            form_rendered = form.render()

        #self.request.response.headers['do_tidy'] = 'yes'

        # import pdb;  pdb.set_trace()

        return {'title': _("Zip Search"),
                'form_title' : _("Download the photos and videos of your flight"),
                'form_rendered' : form_rendered,
                'reqts' : reqts,
               }


    @view_config(route_name='download',
                 renderer='../xhtml/download.xhtml')
    def download(self):
        """ download  """
        zip_id = self.request.matchdict['zip_id']

        class DownloadSchema(colander.Schema):
            """ form schema """
            zip_id = colander.SchemaNode(
                colander.String(),
                widget=deform.widget.TextInputWidget(readonly=True),
                title=_("Identification"),
                name="zip_id",
            )

        def download_form():
            """ return zip id form """
            schema = DownloadSchema()
            schema_zip_id = next(
                (x for x in schema.children if x.name == "zip_id"), None
            )

            #import pdb;  pdb.set_trace()
            #schema_zip_id.default = zip_id
            schema_zip_id.missing = zip_id

            if self.zipstream:
                path = self.request.registry.settings['zipmedia.path'] + zip_id
                exists, ready = utils.status_zipstream(path)
            else:
                path = self.request.registry.settings['zipmedia.path'] + zip_id + ".zip"
                exists, ready = utils.status_zipfile(path)

            if not exists:
                schema_zip_id.description = _("No results found.")
                button_label = deform.Button("back", _("Back"))
            elif not ready:
                schema_zip_id.description = _(
                    "The archive is being processed, please wait")
                button_label = deform.Button("update", _("Update"))
            else:
                schema_zip_id.description = _(
                    "The archive is ready for download")
                button_label = deform.Button("download", _("Download"))

            form = deform.Form(schema,
                               buttons=[button_label],
                               method="post",
                              )
            return form

        form = download_form()
        reqts = form.get_widget_resources()

        # import pdb;  pdb.set_trace()
        if 'download' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
                if self.zipstream:
                    url = self.request.route_url('zipstream',
                                                 zip_id=appstruct['zip_id'])
                else:
                    url = self.request.static_url('zipmedia:zipfile/' +
                                                  appstruct['zip_id'] + ".zip")

                return HTTPFound(url)
            except deform.ValidationFailure as exc:
                # Form is NOT valid
                form_rendered = exc.render()
        elif 'back' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
                url = self.request.route_url('search')
                return HTTPFound(url)
            except deform.ValidationFailure as exc:
                # Form is NOT valid
                form_rendered = exc.render()
        elif 'update' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
                url = self.request.route_url('download',
                                             zip_id=appstruct['zip_id'])
                return HTTPFound(url)
            except deform.ValidationFailure as exc:
                # Form is NOT valid
                form_rendered = exc.render()
        else:
            form_rendered = form.render(appstruct={'zip_id':zip_id})

        return {
            'title': _("Zip Search"),
            'form_title' : _("Download the photos and videos of your flight"),
            'zip_id': zip_id,
            'form_rendered' : form_rendered,
            'reqts' : reqts,
        }


    @view_config(route_name='zipstream',
                 renderer="zip")
    def zip(self):
        """  Return a zip file related to 'id'
        if the zip can not be created then redirect to another web page.
        """
        zip_id = self.request.matchdict['zip_id']

        path = self.request.registry.settings['zipmedia.path'] + zip_id

        exists, ready = utils.status_zipstream(path)

        if not exists or not ready:
            url = self.request.route_url('download',
                                         zip_id=zip_id)
            return HTTPFound(url)

        filename = zip_id + '.zip'
        self.request.response.content_disposition = 'attachment;filename=' + filename

        return {
            'path': path,
        }

# For Emacs:
# Local Variables:
# mode: python
# coding: utf-8
# End:
