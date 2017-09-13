#!/usr/bin/python

import subprocess
import shlex

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