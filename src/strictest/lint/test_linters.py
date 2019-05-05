
import subprocess

def test_isort():
    isort_args = ['isort', '--recursive', '--check-only', '--multi-line=3', '--trailing-comma']
    isort_result = subprocess.run(args=isort_args)
    assert isort_result.returncode == 0

