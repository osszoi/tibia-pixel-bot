import subprocess


def check_process_running(process_name):
    try:
        output = subprocess.check_output(["tasklist"], text=True)
        return process_name in output
    except subprocess.CalledProcessError:
        return False
