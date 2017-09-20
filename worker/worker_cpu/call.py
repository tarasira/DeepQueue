import sys
import subprocess 
ps = subprocess.Popen(('cat', 'main.py'), stdout=subprocess.PIPE)
output = subprocess.check_output(('docker', 'run', '-i', 'tfworker'), stdin=ps.stdout)
ps.wait()
print(output)