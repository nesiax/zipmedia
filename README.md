# zipmedia
A web app to publish and compress on the fly directories

This is a simple pyramid app that allows you to serve directories compressed as zip files.

The zip file can be created on memory or served by an already created .zip file, see production.ini

The app is localized in english and spanish

You can add your own localizations using GNU gettext (.mo files) see i18n.txt and i18n.sh

The zip files can be served using this app (on the fly or static) or you can delegate the function to your webserver on a specific location.

The app works also behind a web server thourhg https. (Only tested on nginx).

<img src="doc/screenshoots/search.png" alt="drawing" width="400"/>

Pyramid: https://trypyramid.com/
Chameleon: https://chameleon.readthedocs.io/en/latest/
ZipStream: https://pypi.org/project/zipstream/

TODO

Test the new zipstream-new https://pypi.org/project/zipstream-new/
