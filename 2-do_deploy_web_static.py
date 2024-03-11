#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os
from fabric.api import local, runs_once, env, put, run
from datetime import datetime

env.user = "ubuntu"
env.hosts = ["100.25.188.244", "34.229.55.60"]


def do_pack():
    """
    Targging project directory into a packages as .tgz
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    local('sudo mkdir -p ./versions')
    path = './versions/web_static_{}'.format(now)
    local('sudo tar -czvf {}.tgz web_static'.format(path))
    name = '{}.tgz'.format(path)
    if name:
        return name
    else:
        return None

def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    """

 if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder = file_name.replace(".tgz", "")
    path = "/data/web_static/releases/{}/".format(folder)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(path, path))
        run("rm -rf {}web_static".format(path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success
