import os
import shutil
import zipfile
import PyInstaller.__main__

program_name = "mlb_data_converter"
version = "1.0"

def build():
    # Remove existing build and dist directories
    if os.path.isdir("build"):
        shutil.rmtree("build")
    if os.path.isdir("dist"):
        shutil.rmtree("dist")

    # Build the exe
    PyInstaller.__main__.run([
        'app\\main.py',
        f'--name={program_name}',
        '--add-data=app\\README;.',
        '--onedir',
        '--noconsole'
    ])

    # Zip up the dist
    zip_file = zipfile.ZipFile(f'dist\\{program_name}-v{version}.zip', 'w', zipfile.ZIP_DEFLATED)
    zip_dir(f'dist\\{program_name}', zip_file)
    zip_file.close()


def zip_dir(path: str, zip_file):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_file.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                           os.path.join(path, '..')))


if __name__ == '__main__':
    build()
