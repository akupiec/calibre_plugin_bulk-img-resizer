import os
import re
import sys
import zipfile

import __version__


def zipdir(path, ziph):
    """
    Zip the contents of an entire directory (including subdirectories).

    :param path: Path of the directory to zip.
    :param ziph: ZipFile handle.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            ziph.write(filepath, os.path.relpath(filepath, os.path.dirname(path)))

def create_zip(zip_filename, paths):
    """
    Create a zip archive containing the files and directories in paths.

    :param zip_filename: Name of the zip file to create.
    :param paths: List of filenames and directory paths to include in the zip archive.
    """
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in paths:
            if os.path.isfile(path):
                zipf.write(path, os.path.basename(path))
            elif os.path.isdir(path):
                zipdir(path, zipf)
            else:
                print(f"Path {path} does not exist and will be skipped.")
    print(f"Created zip file {zip_filename} containing {len(paths)} items.")

def check_if_file_exists(filename):
    if os.path.isfile(filename):
        print(f"File '{filename}' exists. Exiting program.")
        sys.exit(1)

def generate_file_name():
    pattern = re.compile(r"plugin-import-name-(.*)\.txt")

    for file_name in os.listdir('../'):
        match = pattern.match(file_name)
        if match:
            return '../out/' + match.group(1) + '_' + __version__.__version__ + '.zip'


os.makedirs('../out', exist_ok=True)
files_to_zip = []
ignored_stuff = ['.git', '.github', '.gitignore', '.idea', 'dev', 'out', '__pycache__']


entries = os.listdir('../')
for entry in entries:
    if not ignored_stuff.__contains__(entry):
        files_to_zip.append('../' + entry)

zip_filename = generate_file_name()
check_if_file_exists(zip_filename)

create_zip(zip_filename, files_to_zip)
