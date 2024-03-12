#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
#!/usr/bin/python3
"""web server distribution"""
from fabric.api import *
import os.path

env.user = 'ubuntu'
env.hosts = ["3.84.237.53","34.227.91.94"]
env.key_filename = "~/.ssh/school"

def do_deploy(archive_path):
    """distributes an archive to your web servers
    """
    if os.path.exists(archive_path) is False:
        return False
    try:
        arc = archive_path.split("/")
        base = arc[1].strip('.tgz')
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}'.format(base))
        main = "/data/web_static/releases/{}".format(base)
        run('tar -xzf /tmp/{} -C {}/'.format(arc[1], main))
        run('rm /tmp/{}'.format(arc[1]))
        run('mv {}/web_static/* {}/'.format(main, main))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ "/data/web_static/current"'.format(main))
        return True
    except:
        return False
