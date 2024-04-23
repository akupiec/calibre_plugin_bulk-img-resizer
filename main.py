#!/usr/bin/env python
# vim:fileencoding=utf-8

__license__ = 'MIT'
__copyright__ = '2024, Artur Kupiec'

from calibre.ebooks.oeb.base import JPEG_MIME, PNG_MIME, WEBP_MIME
from calibre.gui2 import error_dialog

from calibre.gui2.tweak_book.plugin import Tool
from calibre.ebooks.oeb.polish.replace import rename_files
from qt.core import QAction, QInputDialog, QProgressDialog, Qt, QTimer, QMessageBox
from PIL import Image
import io
import os

from calibre_plugins.bulk_img_reducer.custom_dialog import CustomDialog


def rescale_image(img_data, max_px_size, quality, webp):
    image = Image.open(io.BytesIO(img_data))
    w = float(image.size[0])
    h = float(image.size[1])
    if w < h:
        if w > max_px_size:
            new_w = max_px_size
            scale = max_px_size / w
            new_h = h * scale
        else:
            new_h = h
            new_w = w
    else:
        if h > max_px_size:
            new_h = max_px_size
            scale = max_px_size / h
            new_w = w * scale
        else:
            new_h = h
            new_w = w

    re_image = image.resize((int(new_w), int(new_h)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()

    if webp is True:
        re_image.save(buf, format='webp', quality=quality)
    else:
        re_image.save(buf, format=image.format, quality=quality)

    return buf.getvalue()


def replace_extension(file_name, new_extension):
    base_name, _ = os.path.splitext(file_name)
    return base_name + new_extension


class BulkImgReducer(Tool):
    #: Set this to a unique name it will be used as a key
    name = 'bulk-img-reducer'

    #: If True the user can choose to place this tool in the plugins toolbar
    allowed_in_toolbar = True

    #: If True the user can choose to place this tool in the plugins menu
    allowed_in_menu = True

    RASTER_IMAGES = {JPEG_MIME, PNG_MIME, WEBP_MIME}

    def __init__(self):
        self.config = None
        self.job_data = None
        self.pd_timer = QTimer()

    def create_action(self, for_toolbar=True):
        # Create an action, this will be added to the plugins toolbar and
        # the plugins menu
        ac = QAction(get_icons('images/icon.png'), 'Bulk image resize', self.gui)  # noqa
        if not for_toolbar:
            # Register a keyboard shortcut for this toolbar action. We only
            # register it for the action created for the menu, not the toolbar,
            # to avoid a double trigger
            self.register_shortcut(ac, 'bulk-img-reducer', default_keys=('Ctrl+Shift+Alt+D',))
        ac.triggered.connect(self.ask_user)
        return ac

    def ask_user(self):
        dialog = CustomDialog()

        if dialog.exec_() != CustomDialog.Accepted:
            return

        self.config = dialog.max_resolution, dialog.quality, dialog.covert_to_webp

        self.boss.commit_all_editors_to_container()
        self.boss.add_savepoint('Before: Resizing images')
        self.mimify_images()

    def mimify_images(self):

        self.pd_timer.timeout.connect(self.do_one)

        container = self.current_container  # The book being edited as a container object
        images = self.get_images_from_collection(container)
        print('image_count', len(images))
        if len(images) == 0:
            dialog = QMessageBox()
            dialog.setText('No images found!')
            return

        progress = self.create_progres_dialog(len(images))
        self.job_data = (images, images.copy(), progress, container)
        self.pd_timer.start()

    def get_images_from_collection(self, container):
        images = []
        for name, media_type in container.mime_map.items():
            if media_type in self.RASTER_IMAGES:
                print('files: ' + str(name) + ' mime types:' + str(media_type))
                images.append(name)

        return images

    def create_progres_dialog(self, image_count):
        progress = QProgressDialog('Resizing images...', _('&Stop'), 0, image_count + 1, self.gui)
        progress.setWindowTitle('Resizing...')
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setValue(0)
        progress.show()
        return progress

    def do_one(self):
        try:
            images, all_images, progress, container = self.job_data
            max_resolution, quality, covert_to_webp = self.config
            if len(images) == 0 or progress.wasCanceled():
                self.pd_timer.stop()
                self.do_end()
                return

            name = images.pop()
            new_image = rescale_image(container.parsed(name), max_resolution, quality, covert_to_webp)
            container.replace(name, new_image)
            index = len(all_images) - len(images)
            progress.setValue(index)
        except Exception:
            import traceback
            error_dialog(self.gui, _('Failed to resize images'),
                         _('Failed to resize images, click "Show details" for more info'),
                         det_msg=traceback.format_exc(), show=True)
            self.boss.revert_requested(self.boss.global_undo.previous_container)
            self.pd_timer.stop()

    def do_end(self):
        _, _, convert_to_webp = self.config
        _, all_images, progress, container = self.job_data

        if convert_to_webp is True:
            progress.setWindowTitle('Renaming files...')
            replace_map = {}
            for name in all_images:
                value = os.path.splitext(name)[0] + '.webp'
                replace_map[name] = value
            rename_files(container, replace_map)

        progress.setValue(len(all_images) + 1)

        self.boss.show_current_diff()
        self.boss.apply_container_update_to_gui()
