# sarctransform

Program to scan [School Accountability Report Card (SARC)](https://www.cde.ca.gov/ta/ac/sa/) files
and print ethnic statistics about a school

## Setup and usage

First you need to download the data.
These commands should do the trick within a bash shell
assuming that you have wget and unzip installed:

```sh
wget --recursive --no-parent --no-clobber http://www3.cde.ca.gov/researchfiles/sarc/
wget https://web.archive.org/web/20110124001555/http://www3.cde.ca.gov/researchfiles/sarc/sarc07.zip
wget https://web.archive.org/web/20110124001554/http://www3.cde.ca.gov/researchfiles/sarc/sarc08.zip
wget https://web.archive.org/web/20110124001553/http://www3.cde.ca.gov/researchfiles/sarc/sarc09.zip
unzip sarc07.zip -d sarc07
unzip sarc08.zip -d sarc08
unzip sarc09.zip -d sarc09
```

Then you download the python dependencies
(python is assumed to be installed):

```sh
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

Then you can run the command
```sh
python -m sarctransform --school=lowell
```

## Contributing

Remember to do this before each commit:

```
mypy -m sarctransform
black *.py
```
