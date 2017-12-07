import os
import sys
import commands

def main():
	PROCESSING_DIR = sys.argv[1]
	INPUT_DIR = sys.argv[2]
	AMPS_DIR = sys.argv[3]
	OUT_DIR = sys.argv[4]

	output = open(OUT_DIR, "w")
	AMPs = open(AMPS_DIR, "r")

	for line in AMPs:
		line = line.replace("\n", "")
		data = line.split("\t")
		chrom = data[0]
		start = int(data[1])
		end = int(data[2])
		amp_name = data[3]

		cmd = "%s/view.sh %s '%s:%s-%s'" % (PROCESSING_DIR, INPUT_DIR, chrom, start, end)
		status, ID = commands.getstatusoutput(cmd)

		output.write("%s\t%s\n" % (amp_name, ID))

	AMPs.close()
	output.close()

if __name__ == '__main__':
	main()