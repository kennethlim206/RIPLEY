import os
import sys
import commands
import datetime

def get_names(directory):
	names_list = os.listdir(directory)
	return_list = []

	for name in names_list:
		if name[0] != ".":
			return_list.append(name)
	return return_list

def path_finder(directory, suffix):
	cmd = "find %s -type f -name '*%s'" % (directory, suffix)
	status, sdout = commands.getstatusoutput(cmd)
	if status == 0:
		return sdout.split("\n")
	else:
		sys.exit("ERROR: incorrect path_finder input. Shell says %s" % sdout)

def dependency(x):
	print "Is the job you selected dependent upon the previous job? (Y/N)\n"
	answer = raw_input(">>> ")
	if answer == "Y":
		job_id = raw_input("\nYou entered Yes. Input job ID that the selected jobs will be dependent upon.\n\n> ")
		return [int(job_id), x]
	elif answer == "N":
		print "\nYou entered No. Selected jobs will run independent of any previous jobs."
		return ["default", x]
	else:
		sys.exit("\nERROR: incorrect input to dependency query.")

def make_cmd(time, job_name, job_file, job_vars, slurmOutput_dir, slurmError_dir, dependency_list, partition, cpu_per_task, mem_per_cpu):
	cmd = "sbatch"
	cmd += " --time=%s" % time
	cmd += " --job-name=%s" % job_name
	cmd += " --output=%s.out" % slurmOutput_dir
	cmd += " --error=%s.err" % slurmError_dir

	if dependency_list[0] != "default":
		if dependency_list[1] == "ok":
			cmd += " --dependency=afterok:%s" % str(dependency_list[0])
		elif dependency_list[1] == "any":
			cmd += " --dependency=afterany:%s" % str(dependency_list[0])
	if partition != "default":
		cmd += " --partition=%s" % partition
	if cpu_per_task != "default":
		cmd += " --cpus-per-task=%s" % cpu_per_task
	if mem_per_cpu != "default":
		cmd += " --mem-per-cpu=%s" % mem_per_cpu

	cmd += " %s" % job_file
	if job_vars != "default":
		for var in job_vars:
			var = str(var)
			cmd += " %s" % var

	return cmd

def submit(cmd, name):
	print "Submitting %s ..." % name
	status, ID = commands.getstatusoutput(cmd)
	#status = 0
	#ID = "Submitting job as 1738"
	if status == 0:
		ID_split = ID.split(" ")
		ID = int(ID_split[3])
		print "Job %s submitted as %i" % (name, ID)
		print "Woot! Slurm will take it from here! :)"
	else:
		print "ERROR!"
		print "------- SLURM SAYS -------\n%s" % ID
		print "--------------------------"
		sys.exit()

	return ID

def record(cmd, ID, file_path):
	file = open("%s/slurm_record.txt" % file_path, "a")

	file.write("Sumbitted on: %s\n" % datetime.datetime.now().strftime("%m.%d.%Y %H:%M:%S"))
	file.write("Job ID Number: %s\n" % ID)
	file.write("Submitted with command: %s\n" % cmd)
	file.write("\n-------------------------------\n\n")

	file.close()