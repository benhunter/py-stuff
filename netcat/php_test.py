import subprocess

# command = 'php -r \'$rnd = mt_rand(1, 1); srand(time()); $rnd &= rand(); echo $rnd;\''
command = 'php -r \'mt_srand(1000); $rnd = mt_rand(); echo $rnd;\''
cmd_output = subprocess.check_output(command, shell=True)

print(cmd_output)
