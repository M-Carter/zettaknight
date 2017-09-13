#!/usr/bin/python

import shlex
import subprocess


def spawn_job(cmd):

    try:
        cmd_run = subprocess.Popen(shlex.split(cmd), stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        cmd_run.wait()
        cmd_run_stdout = cmd_run.stdout.read()
        return_code = cmd_run.returncode

        if return_code is not 0:
            raise Exception('{0}: {1}'.format(return_code, cmd_run_stdout))

    except Exception as e:
        raise Exception('FAILED {0}: {1}'.format(cmd, e))

    return cmd_run_stdout


disk_list = []

mpath_out = spawn_job('multipath -ll')
mpath_out = mpath_out.split('\n')

try:
    for line in mpath_out:
        line = line.split()

        if "sd" in line[2]:
            disk_list.append(line[2])

except Exception, e:
    print e
    pass

disk_args = ','.join(disk_list)
print("ledctl failure='{0}'".format(disk_args))
