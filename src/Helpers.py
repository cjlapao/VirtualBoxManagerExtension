import sys
import subprocess

class File:

    @staticmethod
    def executeCmd(path, args = []):
        cmd = path
        if args:
            cmd += " "
            for arg in args:
                cmd += arg
        cmd = subprocess.Popen(cmd, shell=True,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)
        output, error = cmd.communicate()
        if isinstance(output, bytes):
            if output:
                return True, output
            else:
                return False, None
        else:
            if isinstance(error,bytes):
                return False, error.decode("utf8").strip()
            return False, None
