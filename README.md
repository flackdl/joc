# JOC

## Developing

#### Dependencies

- python 3.6
- lxml

Make sure you have python 3.6+ by running

    python --version

Your system may use `python3`, so try:

    python3 --version

For lxml:

 - on linux, make sure you have `python3-lxml`
 - on macos, make sure you have `py36-lxml` from mac ports

#### Create your python environment

This creates a separate python environment in `~/.envs/joc`:

    python3 -mvenv ~/.envs/joc

#### Activate your python environment

    source ~/.envs/joc/bin/activate

You'll now be using the `joc` python environment

#### Install requirements

Now that you've activated the `joc` python environment, you can just run `python` and `pip` and it'll be pointing
to your new environment (vs the global install).

Install all requirements:

    pip install -r requirements.txt

#### Initialize application

Create database tables:

    python manage.py migrate

Create super user (this lets you log into the backend admin):

    python manage.py createsuperuser

#### Import JOC into database

Import joc epub (it must already be unzipped) into database:

    python manage.py import /path/to/extracted/epub-directory

The import script expects to find the `toc.ncx` (table of contents) in the epub directory so make sure you're pointing to the correct place.

#### Start development server

    python manage.py runserver

The server will now be running:

- Backend Admin: [http://127.0.0.1:8000/admin]
- API: [http://127.0.0.1:8000/api]
