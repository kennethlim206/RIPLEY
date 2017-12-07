import sys
import os
import lib.RIPLEY_class as RIPLEY_class

def main():

	print "\n"
	print "**************************************************************************************"
	print "***********                                                                ***********"
	print "***********                                                                ***********"
	print "*********** WELCOME TO RIPLEY! THE NORDLAB's RNA-SEQ INTERACTIVE PIPELINE! ***********"
	print "***********                                                                ***********"
	print "***********                                                                ***********"
	print "**************************************************************************************"

	print "\n"

	exit_1 = 0
	exit_2 = 0
	
	while not exit_1:

		# READ IN INPUT AND SLURM VARIABLES AND SAVE INTO LISTS
		print "-------------------------------------------------------------"
		print "PLEASE ENTER THE NAME OF YOUR INPUT VARS TEXT FILE OR EXIT:"

		input_files = os.listdir("./user_inputs")
		input_files.sort()
		for file in input_files:
			if "input_vars" in file and "BLANK" not in file:
				print file

		print "\nexit"
		print "-------------------------------------------------------------\n"

		x = raw_input(">>> ")

		if x == "exit":
			sys.exit("Ending instance...")

		input_vars = "./user_inputs/%s" % x

		# Error for non-existing user input
		if not os.path.isfile(input_vars):
			sys.exit("ERROR: inputted input_vars does not exist.")

		print "You selected the input file: %s\n" % x

		while not exit_2:

			print "-------------------------------------------------------------"
			print "PLEASE CHOOSE AN ACTION BELOW AND HIT ENTER:\n"

			print "1. Pre Processing Options:"
			print "pull = pull data"
			print "convert = convert .sra files to .fastq"
			print "custom = customize\n"

			print "2. STAR Options:"
			print "index = index reference genome"
			print "align = align to sample fastq data\n"

			print "3. Post Processing Options:"
			print "fqc = fastqc"
			print "rqc = rseqc"
			print "th = trackhub (not implemented)"
			print "feature = subread feature count"
			print "pile = samtools mpileup"
			print "total = samtools view"
			print "multicov = bedtools multicov\n"

			print "exit = exit"
			print "-------------------------------------------------------------\n"
			
			user_input = raw_input(">>> ")

			pre = "false"
			if user_input == "pull" or user_input == "convert":
				pre = "true"

			RIPLEY = RIPLEY_class.RIPLEY_INSTANCE(input_vars, pre)

			if user_input == "exit":
				sys.exit("Ending instance...")

			elif user_input == "pull":
				print "You selected pull data. Running your chosen action...\n"
				RIPLEY.pull_data()
			elif user_input == "convert":
				print "You selected convert data. Running your chosen action...\n"
				RIPLEY.convert2fastq()
			elif user_input == "custom":
				print "You selected customize. Running your chosen action...\n"
				RIPLEY.make_custom()
			elif user_input == "index":
				print "You selected index. Running your chosen action...\n"
				RIPLEY.make_index()
			elif user_input == "align":
				print "You selected align. Running your chosen action...\n"
				RIPLEY.make_align()
			elif user_input == "feature":
				print "You selected feature counts. Running your chosen action...\n"
				RIPLEY.make_feature()
			elif user_input == "pile":
				print "You selected samtools mpileup. Running your chosen action...\n"
				RIPLEY.make_mpileup()
			elif user_input == "redo pile":
				print "You selected samtools mpileup. Running your chosen action...\n"
				RIPLEY.redo_mpileup()
			elif user_input == "total":
				print "You selected samtools view totals. Running your chosen action...\n"
				RIPLEY.make_totals()
			elif user_input == "multicov":
				print "You selected bedtools multicov totals. Running your chosen action...\n"
				RIPLEY.make_multicov()
			elif user_input == "fqc":
				print "You selected fastqc. Running your chosen action...\n"
				RIPLEY.make_fastqc()
			elif user_input == "rqc":
				print "You selected rseqc. Running your chosen action...\n"
				RIPLEY.make_rseqc()
			elif user_input == "th":
				print "You selected trackhub. Running your chosen action...\n"
				RIPLEY.make_trackhub()
			else:
				sys.exit("ERROR: Incorrect command inputted to run_MASTER.py.")

			print "-------------------------------------------------------------\n"
			print "Are there other actions you want to run on this dataset %s (Y/N)?\n" % x
			more_2 = raw_input(">>> ")

			if more_2 == "N":
				exit_2 = 1
			elif more_2 == "Y":
				exit_1 = 0
				exit_2 = 0
			else:
				sys.exit("Incorrect input. Exiting program...")

		print "-------------------------------------------------------------\n"
		print "Are there other actions you want to run on a different dataset (Y/N)?\n"
		more_1 = raw_input(">>> ")

		if more_1 == "N":
			exit_1 = 1
		elif more_1 == "Y":
				exit_1 = 0
				exit_2 = 0
		else:
			sys.exit("Incorrect input. Exiting program...")

if __name__ == '__main__':
	main()