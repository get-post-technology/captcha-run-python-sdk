import subprocess

source_dirs = "captcharun tests"
subprocess.check_call(f"isort --check --diff {source_dirs}", shell=True)
subprocess.check_call(f"black --check --diff {source_dirs}", shell=True)
