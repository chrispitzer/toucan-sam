from __future__ import with_statement
from fabric.api import run, cd, sudo, settings
from fabric.api import local as run_local
from fabric.state import env
from fabric.contrib.files import exists
from os.path import join as _j

env.project_name = 'toucansam'
env.git_repo = 'git@zim.lofiart.com:toucan-sam.git'


def _common():
    env.path = _j('/srv', env.project_name, env.deploy_level)
    env.app_dir = _j(env.path, "app")
    env.server_config_toplevel = _j(env.path, env.project_name, 'server-config')
    env.server_config_dir = _j(env.server_config_toplevel, env.deploy_level)
    env.sys_user = env.deploy_level + '_toucansam'
    env.sys_group = 'deployers'
    env.repo_root = _j(env.path, env.project_name)

def staging():
    "deploy to staging"
    env.hosts = ['gir.lofiart.com']
    env.deploy_level = 'staging'
    _common()

def live():
    "deploy to live"
    env.hosts = ['gir.lofiart.com']
    env.deploy_level = 'live'
    _common()

def git_update():
    "Update the remote git repo (requires a tag to update to)"
    pull_cmd = 'cd %s; git pull' % env.repo_root
    run_local("ssh -A %s '%s'" % (env.host_string, pull_cmd))

def copy_configs():
    "Copy server configs into place"
    with cd(env.server_config_toplevel):
        run('cp %s/local_settings.py %s/' % (env.server_config_dir, env.app_dir))
        run('cp %s/gunicorn.conf %s/' % (env.server_config_dir, _j(env.path, 'conf')))
        sudo('cp %s/nginx.conf %s' % (env.server_config_dir, '/etc/nginx/sites-available/%s-%s.conf' % (env.project_name, env.deploy_level)))
        sudo('cp %s/supervisor.conf %s' % (env.server_config_dir, '/etc/supervisor/conf.d/%s-%s.conf' % (env.project_name, env.deploy_level)))
        run('cp %s/bash_profile %s/.bash_profile' % (env.server_config_dir, env.path))
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
    # make all permissions be user: staging_toucansam, group: deployers, g+w
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

