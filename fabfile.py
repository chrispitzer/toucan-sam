from __future__ import with_statement
from fabric.api import run, cd, sudo, settings
from fabric.api import local as run_local
from fabric.state import env
from fabric.contrib.files import exists
from os.path import join as _j

env.project_name = 'toucan'
env.git_repo = 'git@zim.lofiart.com:toucan-sam.git'



def setup():
    """
    PRINTS OUT YOUR TODO LIST FOR SYSTEM SETUP

    """

    print """
    1) create folders
        - create the following directories on the server: (owner doesn't matter yet)
        # NOTE: env.project name (from above) needs to match [project_name] below
            - /srv
            - /srv/[project_name]
            - /srv/[project_name]/staging
            - /srv/[project_name]/staging/logs
            - /srv/[project_name]/staging/conf
            - /srv/[project_name]/staging/sock
            - /srv/[project_name]/staging/media (if you're using a media root at all)

            # repeat for /srv/[project_name]/live/...

    2) create users
        - create staging and live users on the server, by running the following commands
            $ sudo adduser --disabled-password --disabled-login --shell /bin/bash --home /srv/[project_name]/staging --no-create-home --gecos ,,,,, staging_[project_name] # creates staging_foo_bar
            $ sudo adduser --disabled-password --disabled-login --shell /bin/bash --home /srv/[project_name]/live --no-create-home --gecos ,,,,, live_[project_name] # creates live_foo_bar

    2.5) reset permissions
        run: fab staging reset_permissions (and live)
        expect errors from static (doesn't exist yet) and .bash_profile (hasn't been copied over yet)

    3) create virtual env
        $ sudo -s # become root
        $ su - staging_[project_name] # become staging user
        $ virtualenv /srv/[project_name]/staging/env # create venv
        # activate the virtualenv
        $ pip install gunicorn

        # ... repeat for "live" user.

    4) install system apps

        - make sure nginx and supervisor are installed
            $ sudo apt-get install nginx supervisor
        - make sure the correct conf directories exist:
            - /etc/nginx/sites-available
            - /etc/supervisor/conf.d

    5) git
        - make sure the server has git
        - make sure you can ssh to zim (or the git repo) from the server
            - your user's ssh config needs to have "ForwardAgent yes"

    6) add to repo
        - create your server_config directory in your repo, follow the pattern from another project
          all files in server_config have paths that need to be set. That's where all the configs for nginx, gunicorn, bash_profile, supervisor, etc exist.
           - NOTE: you need bash_profile to make gunicorn work.
           - NOTE: when you are setting up nginx.conf, you will need server_name to match the domain you want nginx to serve for.

    7) database
        $ sudo -s
        $ su - postgres

        - create the database users you'll need for staging and live
            $ createuser staging_[project_name] # repeat for live, and "no" to all questions

        - create the databases you'll need for staging and live
            $ createdb staging_[project_name] # repeat for live

        - give the database users ownership or permission to edit their database
            - for postgres:
                $ psql
                $ alter database <name> owner to <owner>;

        - auth of some kind...
            - password:
                - set db passwords, and make sure those passwords are mirrored in local_settings.py files in server-config in your repo
            - OR ident (no passwords):
                - remove password, host, and port form db settings in server-config

    7.5) code, etc
        - Get the code. #for both staging and live:
            # as YOU, not as root...
            - clone the repo into /srv/[project_name]/staging/[project_name]
            # NOTE: make sure .../staging/... is on the "develop" branch, and .../live/... is on the "master" branch.
        - other stuff...
            - symlink /srv/[project_name]/staging/app -> /srv/[project_name]/staging/[project_name]/path/to/manage.py/directory
            - make local settings for the server have STATIC_ROOT be /srv/[project_name]/staging/static (for staging, and live for live)

    8) go go go
        - run fab staging reset_permissions
        - run fab staging deploy
        - repeat as necessary

    9) turn on nginx for the site
        symlink /etc/nginx/sites-available/staging_[project_name].conf -> /etc/nginx/sites-enabled/staging_[project_name].conf
        run: fab staging restart_services

        """


def _common():
    env.path = _j('/srv', env.project_name, env.deploy_level)
    env.app_dir = _j(env.path, "app")
    env.server_config_toplevel = _j(env.path, env.project_name, 'server-config')
    env.server_config_dir = _j(env.server_config_toplevel, env.deploy_level)
    env.sys_user = env.deploy_level + '_toucan'
    env.sys_group = 'deployers'
    env.repo_root = _j(env.path, env.project_name)
    env.forward_agent = True

def staging():
    "deploy to staging"
    env.hosts = ['dib.lofiart.com']
    env.deploy_level = 'staging'
    _common()

def live():
    "deploy to live"
    env.hosts = ['dib.lofiart.com']
    env.deploy_level = 'live'
    _common()

def git_update():
    "Update the remote git repo (requires a tag to update to)"
    with cd(env.repo_root):
        run('git pull')

def copy_configs():
    "Copy server configs into place"
    with cd(env.server_config_toplevel):
        run('cp %s/local_settings.py %s/toucansam/' % (env.server_config_dir, env.app_dir))
        run('cp %s/gunicorn.conf %s/' % (env.server_config_dir, _j(env.path, 'conf')))
        sudo('cp %s/nginx.conf %s' % (env.server_config_dir, '/etc/nginx/sites-available/%s-%s.conf' % (env.project_name, env.deploy_level)))
        sudo('cp %s/supervisor.conf %s' % (env.server_config_dir, '/etc/supervisor/conf.d/%s-%s.conf' % (env.project_name, env.deploy_level)))
        run('cp %s/bash_profile %s/.bash_profile' % (env.server_config_dir, env.path))
        if False: # TODO: this should get wrapped up in something checking to see if the crontab exists
            sudo('su - %s -c "crontab %s/crontab"' % (env.sys_user, env.server_config_dir))

def restart_services(service='both'):
    "reload nginx config, restart gunicorn"
    # reload nginx, restart supervisord
    if service in ('both', 'nginx'):
        sudo('/etc/init.d/nginx reload')
    if service in ('both', 'gunicorn'):
        sudo('supervisorctl reload')
        import time
        time.sleep(1)
        sudo('supervisorctl restart %s_%s' % (env.deploy_level, env.project_name))

def reset_permissions():
    "reset all permissions"
    # make all permissions be user: staging_toucan, group: deployers, g+w
    with cd(env.path):
        with settings(warn_only=True):
            sudo('chown %s:%s .' % (env.sys_user, env.sys_group))
            sudo('chmod -R g+w .')
            sudo('chown -R %s:%s *' % (env.sys_user, env.sys_group))
            sudo('chmod -R g+w *')
            sudo('chgrp -R www-data %s/media' % env.path)
            sudo('chmod -R o+r %s/static' % env.path)
        sudo('chown %s:%s .bash_profile' % (env.sys_user, env.sys_group))
        sudo('chmod -R g+w .bash_profile')

def run_migrations():
    "run migrations"
    syncdb_cmd = "cd %s; python manage.py syncdb --noinput" % env.app_dir
    migrate_cmd = "cd %s; python manage.py migrate" % env.app_dir
    sudo('su - %s -c "%s"' % (env.sys_user, syncdb_cmd))
    sudo('su - %s -c "%s"' % (env.sys_user, migrate_cmd))


def install_requirements():
    "install requirements from requirements.txt"
    sudo('su - %s -c "pip install -r %s/requirements.txt"' % (env.sys_user, _j(env.path, env.project_name)))

def collectstatic():
    sudo('su - %s -c "cd %s; ./manage.py collectstatic --noinput"' % (env.sys_user, env.app_dir))

def deploy():
    "Deploy all-in-one -- requires a tag to update git to"
    git_update()
    copy_configs()
    install_requirements()
    run_migrations()
    collectstatic()
    reset_permissions()
    restart_services()

