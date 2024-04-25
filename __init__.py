#!/usr/bin/env python
# vim:fileencoding=utf-8


__license__ = 'MIT'

from calibre.customize import EditBookToolPlugin


class BulkImgReducerPlugin(EditBookToolPlugin):

    name = 'Bulk img resizer'
    version = (1, 1, 0)
    author = 'Artur Kupiec'
    supported_platforms = ['windows', 'osx', 'linux']
    description = 'Resize all images and keep them under specified resolution'
    minimum_calibre_version = (7, 0, 0)
