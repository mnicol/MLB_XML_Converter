# MLB_XML_Converter
Program to convert MLB xml data to xml that a Tricaster machine can use

# Getting Started
* Pull down data from git repo into a local ide like pycharm
* Set up a virtual environment with python 3.8 or higher
* Run `pip install -r requirements.txt`

# Runing and Building
* To run the app run /app/main.py
* To build the app run pyinstaller.py
    * This will create a `build` and a `dist` folder
    * The dist folder will have a zipped and unzipped version of the program and accompanying files
* pyinstaller.py has variables for the exe name as well as the version number
* More information of using the app, and it's configuration can be found in `/app/README`