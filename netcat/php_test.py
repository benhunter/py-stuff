import subprocess

command = 'php -r \'$rnd = mt_rand(1, 1); srand(time()); $rnd &= rand(); echo $rnd;\''
cmd_output = subprocess.check_output(command, shell=True)

print(cmd_output)
