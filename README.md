# ZipMedia

A web app to publish and compress directories on the fly to be downloaded as zip files.

This is a simple pyramid app that allows you to serve directories compressed as zip files.

The zip file can be created on memory or served by an already created .zip file, see `production.ini`.

The app is localized in english and spanish

You can add your own localizations using GNU gettext (.mo files) see `i18n.txt` and `i18n.sh`.

The zip files can be served using this app (on the fly or static) or you can delegate the function to your webserver on a specific location.

The app works also behind a web server thourhg https. (Only tested on nginx).

## History

I wrote this app to learn about pyramid building a simple app that allows a user to share directories containing photos and videos of 500 MB size in average.

This is useful for someone that will copy the directory to a network share (usually via samba) and let the receiver download the directory or the zip file just using and id.

## Screenshoots

Search:
<img src="doc/screenshoots/search.png" alt="drawing" width="400"/>

Form validation:
<img src="doc/screenshoots/error.png" alt="drawing" width="400"/>

Download:
<img src="doc/screenshoots/search.png" alt="drawing" width="400"/>

i18n spanish:
<img src="doc/screenshoots/search_es.png" alt="drawing" width="400"/>

## Main tools used:

- Pyramid: https://trypyramid.com/
- Chameleon: https://chameleon.readthedocs.io/en/latest/
- ZipStream: https://pypi.org/project/zipstream/
- Bootstrap: https://getbootstrap.com/docs/3.3/
- Deform: https://docs.pylonsproject.org/projects/deform/en/latest/

## TODO

Test the new zipstream-new https://pypi.org/project/zipstream-new/
