#!/usr/bin/python3
""" Fabric script that delete out-of-date archives, using the function do_clean
"""
from fabric.api import *
import os.path
import re
from datetime import datetime

env.user = 'ubuntu'
env.hosts = ["3.84.237.53","34.227.91.94"]
env.key_filename = "~/.ssh/school"


def do_pack():
    """distributes an archive to your web servers
    """
    target = local("mkdir -p ./versions")
    name = str(datetime.now()).replace(" ", '')
    opt = re.sub(r'[^\w\s]', '', name)
    tar = local('tar -cvzf versions/web_static_{}.tgz web_static'.format(opt))
    if os.path.exists("./versions/web_static_{}.tgz".format(opt)):
        return os.path.normpath("./versions/web_static_{}.tgz".format(opt))
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to your web servers
    """
    if os.path.exists(archive_path) is False:
        return False
    try:
        base_filename = os.path.basename(archive_path)
        base = os.path.splitext(base_filename)[0]
        put(archive_path, '/tmp/')
        sudo('mkdir -p /data/web_static/releases/{}'.format(base))
        main = "/data/web_static/releases/{}".format(base)
        sudo('tar -xzf /tmp/{} -C {}/'.format(base_filename, main))
        sudo('rm /tmp/{}'.format(base_filename))
        sudo('mv {}/web_static/* {}/'.format(main, main))
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {}/ "/data/web_static/current"'.format(main))
        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """distributes an archive to your web servers"""
    path = do_pack()
    if path is None:
        return False
    deploy = do_deploy(path)
    return deploy


def do_clean(number=0):
    """Deletes out-of-date archives"""
    if int(number) < 2:
        number = 1  """Keep the most recent version"""
    else:
        number = int(number)

    """ Local clean up"""
    local("ls -t ./versions | tail -n +{} | xargs -I {{}} rm ./versions/{{}}".format(number + 1))

    """Remote clean up"""
    with cd('/data/web_static/releases'):
        sudo("ls -t | tail -n +{} | xargs -I {{}} rm -rf /data/web_static/releases/{{}}".format(number + 1))

