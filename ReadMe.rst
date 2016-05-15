=================
AakashTechSupport
=================

A **WebApp** to provide online *Technical Support* to the people using Aakash tablets.

(Summer Internship 2014, Indian Institute of Technology, Bombay)

Clone
-----

- Make sure your Internet is working. :)
- Clone this repo by typing ::

    git clone https://github.com/darkdefender27/AakashTechSupport.git


Installation
------------

- Install Virtual Environment using the following command ::

    sudo apt-get install python-virtualenv

- Create a Virtual Environment ::

    virtualenv /path/to/virtualenv

- Activate the virtualenv using the command ::

    source /path/to/virtualenv-name/bin/activate

- Change the directory to the `AakashTechSupport/` project using the command ::

    cd /path/to/AakashTechSupport

- Install pre-requisites using the command ::

    pip install -r requirement.txt

  or you can also type ::

    easy_install `cat requirement.txt`


Usage
-----

- Using sqlite3 (For development server only). Though, we recommend to use `MySQL` for deployment
  server. See `settings.py` file for usage.

  Open `AakashTechSupport/AakashTechSupport/settings.py` file and do the following changes ::

    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backend.sqlite3',
        'NAME'  : 'techsupport.db',
        #No need to mention below fields while using sqlite3
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
    }


- Populate the database using the following command ::

    cd /path/to/AakashTechSupport
    python manage.py syncdb

- Run the script populate.py which enters details of remote center into the table Tabletinfo from the details_of_rc.csv file ::
    
    python populate.py

- Start the server using the command ::

    python manage.py runserver


Contributing
------------

- Never edit the master branch.
- Make a branch specific to the feature you wish to contribute on.
- Send me a pull request.
- Please follow `PEP8 <http://legacy.python.org/dev/peps/pep-0008/>`_
  style guide when coding in Python.

License
-------

GNU GPL Version 3, 29 June 2007.

Please refer this `link <http://www.gnu.org/licenses/gpl-3.0.txt>`_
for detailed description.
