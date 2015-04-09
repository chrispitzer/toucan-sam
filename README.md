# Toucan website.

http://toucansamandthefruitloops.com/

## Installation

```
mkvirtualenv env  # If this doesn't work, you should install virtualenv && virtualenvwrapper
pip install -r requirements.txt
cp toucansam/toucansam/local_settings.py{.tmpl,}
# edit toucansam/toucansam/local_settings.py to have correct info for your system
./manage.py syncdb --migrate
./manage.py loaddata dumps/site_data_2013_12_17.json
./runserver.sh
```
