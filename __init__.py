#!/usr/bin/env python
# vim:fileencoding=utf-8


__license__ = 'MIT'

from calibre.customize import EditBookToolPlugin

from calibre_plugins.bulk_img_resizer.__version__ import version_tuple


class BulkImgReducerPlugin(EditBookToolPlugin):

    name = 'Bulk img resizer'
    version = version_tuple
    author = 'Artur Kupiec'
    supported_platforms = ['windows', 'osx', 'linux']
    description = 'Resize all images and keep them under specified resolution'
    minimum_calibre_version = (7, 0, 0)
