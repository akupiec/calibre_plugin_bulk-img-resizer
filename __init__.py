#!/usr/bin/env python
# vim:fileencoding=utf-8


__license__ = 'MIT'
__copyright__ = '2024, Artur Kupiec'

from calibre.customize import EditBookToolPlugin

class BulkImgReducerPlugin(EditBookToolPlugin):

    name = 'Bulk img reducer'
    version = (1, 0, 0)
    author = 'Artur Kupiec'
    supported_platforms = ['windows', 'osx', 'linux']
    description = 'Resize all big images and keep them under specified resolution'
    minimum_calibre_version = (7, 0, 0)
