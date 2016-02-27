import os

AI = 0
Timeout = 0
Random = 0

for i in range(20):
	os.system("python evaluator_code.py 1 > results")

	file = open("results")

	result = file.readline()

	r = result.split(" ")

	if r[0] == "P2":
		AI = AI + 1

	else:
		if r[1] == "TIMED":
			Timeout = Timeout + 1
		else:
			Random = Random + 1

print AI, Timeout, Random