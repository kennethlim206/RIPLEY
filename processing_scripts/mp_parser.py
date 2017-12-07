import os
import sys

# Returns dictionary of nucleotide count pairs
def match_vals(nucs, vals):
	d = {"A":"0", "C":"0", "G":"0", "T":"0", "N":"0", "<*>":"0"}
	for i in range(0,len(nucs)):
		n = nucs[i]
		v = vals[i]
		if n == "A":
			d["A"] = v
		elif n == "C":
			d["C"] = v
		elif n == "G":
			d["G"] = v
		elif n == "T":
			d["T"] = v
		elif n == "N":
			d["N"] = v
		elif n == "<*>":
			d["<*>"] = v
	return d

def get_nuc(d, n):
	if n == d["A"]:
		return "A"
	elif n == d["C"]:
		return "C"
	elif n == d["G"]:
		return "G"
	elif n == d["N"]:
		return "N"
	elif n == d["T"]:
		return "T"
	elif n ==d["<*>"]:
		return "<*>"

def parse(input_path, output_path):
	input_file = open(input_path, "r")
	output_file = open(output_path, "w")
	output_file.write("CHROM\tPOS\tREF\tALT\tREF_VAL\tALT_VAL\tA\tC\tG\tT\tN\tTOTAL\tDP\n")

	for line in input_file:
		line = line.replace("\n", "")
		if "#" not in line:
			data = line.split("\t")

			# Sometimes INDELs are lines
			USE_LINE = data[7].split(";")[0]

			if "DP" in USE_LINE:

				CHROM = str(data[0])
				POS = str(data[1])
				REF = str(data[3])
				DP = USE_LINE.split("=")[1]

				NUCS = data[4].split(",")
				ALT = NUCS[0]
				NUCS.insert(0, REF)
				VALS = data[9].split(":")[1].split(",")

				D = match_vals(NUCS, VALS)

				A = D["A"]
				C = D["C"]
				G = D["G"]
				T = D["T"]
				N = D["N"]
				STAR = D["<*>"]

				TOTAL = int(A) + int(C) + int(G) + int(T) + int(N)

				REF_VAL = D[REF]
				ALT_VAL = D[ALT]

				OUT_VALS = (CHROM, POS, REF, ALT, REF_VAL, ALT_VAL, A, C, G, T, N, TOTAL, DP)
				OUT_STR = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % OUT_VALS

				output_file.write(OUT_STR)
			
	input_file.close()
	output_file.close()

def main():

	parse(sys.argv[1], sys.argv[2])
	# parse("/Users/kennethlim/Desktop/test.txt", "/Users/kennethlim/Desktop/test_parsed.txt")

if __name__ == "__main__":
    main()