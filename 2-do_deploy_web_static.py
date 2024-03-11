#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.

import os
import subprocess as sub
from fabric.api import env, put, run
from datetime import datetime

env.user = "ubuntu"
env.hosts = ["100.25.188.244", "34.229.55.60"]


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    """

    if not os.path.exists(archive_path):
        return False
    try:
        # getting name of archive from archive_path
        temp = str(archive_path).split("/")[-1]
        name = temp.split(".")[0]

        # placing the archive
        sub.run(["scp", "{}".format(archive_path),
                 "{}@{}:/tmp/".format(env.user, env.host)], stdin="yes")
        # put(archive_path, "/tmp/")

        # uncompressing...
        # extraction path
        extrPath = "/data/web_static/releases/{}/".format(name)
        run("mkdir -p {}".format(extrPath))
        run("tar -xzf /tmp/{} -C {}".format(temp, extrPath))
        run("mv {}/web_static/* {}".format(extrPath, extrPath))
        # removing extracted
        run("rm /tmp/{}".format(temp))

        # deletes the symbolic
        run("rm -rf /data/web_static/current")

        # new symbolic link
        run("ln -s {} /data/web_static/current".format(extrPath))
        print("New version deployed!")
        return True
    except Exception as nope:
        print(nope)
        return False
