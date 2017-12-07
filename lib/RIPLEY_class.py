import sys
import os
import commands
import time
import lib.slurm as slurm

class RIPLEY_INSTANCE:
	def __init__ (self, input_vars, pre):
		self.d = {"PROCESSING DIR":"./processing_scripts", "INPUT VARS":input_vars}

		# Always do...
		file = open(input_vars, "r")
		for line in file:
			if line[0] == "$":
				line = line.replace("\n", "")

				if "SRR NAMES" in line:
					data = line.split("=>")[1]
					data = data.replace(" ", "")
					if "#" in data or data == "":
						data = ""
					else:
						data = data.split(",")
					self.d["SRR NAMES"] = data

				if "FTP COMMAND" in line:
					data = line.split("=>")[1]
					data = data.replace(" ", "")
					if "#" in data or data == "":
						data = ""
					else:
						data = data.split(",")
					self.d["FTP COMMAND"] = data

				if "TO DIRECTORY" in line:
					data = line.split("=>")[1]
					data = data.replace(" ", "")
					self.d["SAMPLE DIR"] = data

				if "SINGLE OR PAIRED END DATA" in line:
					data = line.split("=>")[1]
					data = data.replace(" ", "")
					if data != "S" and data != "P":
						sys.exit("ERROR: Incorrect input into SINGLE/PAIRED END READ input var.")
					self.d["SINGLE PAIR"] = data

				if "PAIRED SUFFIX" in line:
					data = line.split("=>")[1]
					data = data.replace(" ", "")
					self.d["PAIRED SUFFIX"] = data
		file.close()

		# Do if pre-processing option not selected
		if pre == "false":
			file = open(input_vars, "r")
			for line in file:
				if line[0] == "$":
					line = line.replace("\n", "")
					
					if "REFERENCE GENOME SELECTION" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")

						REF_FA = ""
						REF_ANNO = ""
						REF_BED = ""
						if data == "0":
							REF_FA = "/share/nordlab/genomes/Homo_sapiens/Gencode/24/FASTA/GRCh38.primary_assembly.genome.fa"
							REF_ANNO = "/share/nordlab/genomes/Homo_sapiens/Gencode/24/Annotations/gencode.v24.annotation.gtf"
							REF_BED = "/share/nordlab/genomes/Homo_sapiens/Gencode/24/Annotations/hg38_knownGene.bed"
						elif data == "1":
							REF_FA = "/share/nordlab/genomes/Homo_sapiens/Gencode/19/FASTA/GRCh37.p13.genome.fa"
							REF_ANNO = "/share/nordlab/genomes/Homo_sapiens/Gencode/19/Annotations/gencode.v19.annotation.gtf"
							REF_BED = "/share/nordlab/genomes/Homo_sapiens/Gencode/19/Annotations/hg19_knownGene.bed"
						elif data == "2":
							REF_FA = "/share/nordlab/genomes/Homo_sapiens/UCSC/hg19/sequence/hg19.fa"
							REF_ANNO = "'GTF file does not exist for this genome yet.'"
							REF_BED = "/share/nordlab/genomes/Homo_sapiens/UCSC/hg19/annotation/hg19_knownGene.bed"
						elif data == "3":
							REF_FA = "/share/nordlab/genomes/Mus_musculus/Gencode/M8/FASTA/GRCm38.primary_assembly.genome.fa"
							REF_ANNO = "/share/nordlab/genomes/Mus_musculus/Gencode/M8/Annotations/gencode.vM8.primary_assembly.annotation.gtf"
							REF_BED = "'BED file does not exist for this genome yet.'"
						elif data == "4":
							REF_FA = "/share/nordlab/genomes/Mus_musculus/Gencode/M1/FASTA/NCBIM37.genome.fa"
							REF_ANNO = "/share/nordlab/genomes/Mus_musculus/Gencode/M1/Annotations/gencode.vM1.annotation.gtf"
							REF_BED = "'BED file does not exist for this genome yet.'"
						elif data == "5":
							REF_FA = "/share/nordlab/genomes/Mus_musculus/Ensembl/GRCm38/Sequence/WholeGenomeFasta/genome.fa"
							REF_ANNO = "/share/nordlab/genomes/Mus_musculus/Ensembl/GRCm38/Annotation/Genes/genes.gtf"
							REF_BED = "/share/nordlab/genomes/Mus_musculus/Ensembl/GRCm38/Annotation/Genes/genes.sorted.bed"
						elif data == "6":
							REF_FA = "/share/nordlab/genomes/Mus_musculus/UCSC/mm10/Sequence/WholeGenomeFasta/genome.fa"
							REF_ANNO = "/share/nordlab/genomes/Mus_musculus/UCSC/mm10/Annotation/Genes/genes.gtf"
							REF_BED = "/share/nordlab/genomes/Mus_musculus/UCSC/mm10/Annotation/Genes/genes.sorted.bed"
						elif data == "7":
							REF_FA = "/share/nordlab/genomes/Mus_musculus/UCSC/mm9/Sequence/WholeGenomeFasta/genome.fa"
							REF_ANNO = "/share/nordlab/genomes/Mus_musculus/UCSC/mm9/Annotation/Genes/genes.gtf"
							REF_BED = "/share/nordlab/genomes/Mus_musculus/UCSC/mm9/Annotation/Genes/mm9_knownGene.bed"
						elif data == "8":
							REF_FA = "/share/nordlab/genomes/Rattus_norvegicus/UCSC/rn5/Sequence/WholeGenomeFasta/genome.fa"
							REF_ANNO = "/share/nordlab/genomes/Rattus_norvegicus/UCSC/rn5/Annotation/Genes/genes.gtf"
							REF_BED = "/share/nordlab/genomes/Rattus_norvegicus/UCSC/rn5/Annotation/Genes/genes.sorted.bed"
						else:
							sys.exit("ERROR: Incorrect input into REFERENCE GENOME SELECTION input var.")

						self.d["REF FA"] = REF_FA
						self.d["REF ANNO"] = REF_ANNO
						self.d["REF BED"] = REF_BED

					if "CUSTOMIZATION" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")

						if data != "T" and data != "F":
							sys.exit("ERROR: Incorrect input into CUSTOMIZE input var.")
						self.d["CUSTOMIZE"] = data

					if "STAR VERSION" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						self.d["STAR MODULE"] = data

					if "OUTPUT FOR INDEX DIRECTORY" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						self.d["INDEX DIR"] = data

					if "REFERENCE GENOME ADDITIONS" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						if "#" in data:
							data = ""
						data = "./customizations/%s" % data
						self.d["ADD FA"] = data

					if "ANNOTATION ADDITIONS" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						if "#" in data:
							data = ""
						data = "./customizations/%s" % data
						self.d["ADD ANNO"] = data

					if "CUSTOM COMBINED GENOME FILE NAME" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						if "#" in data:
							data = ""
						self.d["CUSTOM FA"] = data

					if "CUSTOM COMBINED ANNOTATIONS FILE NAME" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						if "#" in data:
							data = ""
						self.d["CUSTOM ANNO"] = data
					
					if "RUN THREAD N" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						data = int(data)
						self.d["RUN THREAD"] = data

					if "SJBD OVERHANG" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						data = int(data)
						self.d["SJBD OVERHANG"] = data
						self.d["READ LENGTH"] = data + 1

					if "OTHER INDEX PARAMETERS" in line:
						data = line.split("=> ")[1]
						data = data.replace(" ", "", 1)
						if "#" in data:
							data = ""
						if data != "":
							data = "'%s'" % data
						self.d["STAR INDEX PARAMS"] = data

					if "OUTPUT FOR MAPPING DIRECTORY" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						self.d["DATA DIR"] = data

					if "FASTA SUFFIX" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						self.d["FASTA SUFFIX"] = data

					if "ZIPPED" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						ZIP = ""

						if data == ".gz":
							ZIP = "'--readFilesCommand gunzip -c'"
						elif data == ".bzip2":
							ZIP = "'--readFilesCommand bunzip2 -c'"
						elif data == "":
							ZIP = ""
						else:
							sys.exit("ERROR: Incorrect input into ZIPPED input variable")

						self.d["ZIPPED"] = ZIP

					if "OTHER MAPPING PARAMETERS" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "", 1)
						if "#" in data:
							data = ""
						if data != "":
							data = "'%s'" % data
						self.d["STAR ALIGN PARAMS"] = data

					if "SUBREAD VERSION" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						self.d["SUBREAD MODULE"] = data

					if "OTHER FC PARAMETERS" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "", 1)
						if "#" in data:
							data = ""
						if data != "":
							data = "'%s'" % data
						self.d["FC PARAMS"] = data

					if "SAMTOOLS VERSION" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						self.d["SAMTOOLS MODULE"] = data

					if "INPUT AMPLICONS FILE NAME" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "")
						if "#" in data:
							data = ""
						data = "./user_inputs/amplicons/%s" % data
						self.d["AMPLICONS"] = data

					if "OTHER MP PARAMETERS" in line:
						data = line.split("=>")[1]
						data = data.replace(" ", "", 1)
						if "#" in data:
							data = ""
						if data != "":
							data = "'%s'" % data
						self.d["MP PARAMS"] = data

			# DECLARE PRE PROCESSING CUSTOM DIRECTORIES
			if self.d["CUSTOMIZE"] == "T":
				self.d["USE FA"] = "%s/%s" % (self.d["INDEX DIR"], self.d["CUSTOM FA"])
				self.d["USE ANNO"] = "%s/%s" % (self.d["INDEX DIR"], self.d["CUSTOM ANNO"])
			elif self.d["CUSTOMIZE"] == "F":
				self.d["USE FA"] = self.d["REF FA"]
				self.d["USE ANNO"] = self.d["REF ANNO"]
			else:
				sys.exit("ERROR: Incorrect input into input var CUSTOMIZE: %s" % self.d["CUSTOMIZE"])

			# DECLARE POST PROCESSING DIRECTORIES
			self.d["ALIGN DIR"] = "%s/ALIGN" % self.d["DATA DIR"]
			self.d["FEATURECOUNT DIR"] = "%s/FEATURECOUNT" % self.d["DATA DIR"]
			self.d["RAW MP DIR"] = "%s/MP_RAW" % self.d["DATA DIR"]
			self.d["MP DIR"] = "%s/MP_PARSED" % self.d["DATA DIR"]
			self.d["TOTALS DIR"] = "%s/TOTALS" % self.d["DATA DIR"]
			self.d["MULTICOV DIR"] = "%s/MULTICOV" % self.d["DATA DIR"]
			self.d["FASTQC DIR"] = "%s/FASTQC" % self.d["DATA DIR"]
			self.d["RSEQC DIR"] = "%s/RSEQC" % self.d["DATA DIR"]

		file.close()

		# Slurm params
		file = open("./user_inputs/slurm_vars.txt", "r")
		slurm_list = []
		for line in file:
			if line[0] == "$":
				line = line.split("=>")[1]
				line = line.replace(" ", "")
				line = line.replace("\n", "")
				slurm_list.append(line)
		file.close()

		# SBATCH VARIABLES
		i = 0
		self.SBATCH_PULL_T = slurm_list[i]
		i += 1
		self.SBATCH_PULL_P = slurm_list[i]
		i += 1
		self.SBATCH_PULL_C = slurm_list[i]
		i += 1
		self.SBATCH_PULL_MPC = slurm_list[i]
		i += 1

		self.SBATCH_CUSTOM_T = slurm_list[i]
		i += 1
		self.SBATCH_CUSTOM_P = slurm_list[i]
		i += 1
		self.SBATCH_CUSTOM_C = slurm_list[i]
		i += 1
		self.SBATCH_CUSTOM_MPC = slurm_list[i]
		i += 1

		self.SBATCH_INDEX_T = slurm_list[i]
		i += 1
		self.SBATCH_INDEX_P = slurm_list[i]
		i += 1
		self.SBATCH_INDEX_C = slurm_list[i]
		i += 1
		self.SBATCH_INDEX_MPC = slurm_list[i]
		i += 1

		self.SBATCH_ALIGN_T = slurm_list[i]
		i += 1
		self.SBATCH_ALIGN_P = slurm_list[i]
		i += 1
		self.SBATCH_ALIGN_C = slurm_list[i]
		i += 1
		self.SBATCH_ALIGN_MPC = slurm_list[i]
		i += 1

		self.SBATCH_FC_T = slurm_list[i]
		i += 1
		self.SBATCH_FC_P = slurm_list[i]
		i += 1
		self.SBATCH_FC_C = slurm_list[i]
		i += 1
		self.SBATCH_FC_MPC = slurm_list[i]
		i += 1

		self.SBATCH_MP_T = slurm_list[i]
		i += 1
		self.SBATCH_MP_P = slurm_list[i]
		i += 1
		self.SBATCH_MP_C = slurm_list[i]
		i += 1
		self.SBATCH_MP_MPC = slurm_list[i]
		i += 1

		self.SBATCH_FQC_T = slurm_list[i]
		i += 1
		self.SBATCH_FQC_P = slurm_list[i]
		i += 1
		self.SBATCH_FQC_C = slurm_list[i]
		i += 1
		self.SBATCH_FQC_MPC = slurm_list[i]
		i += 1

		self.SBATCH_RQC_T = slurm_list[i]
		i += 1
		self.SBATCH_RQC_P = slurm_list[i]
		i += 1
		self.SBATCH_RQC_C = slurm_list[i]
		i += 1
		self.SBATCH_RQC_MPC = slurm_list[i]
		i += 1

		self.SBATCH_THUB_T = slurm_list[i]
		i += 1
		self.SBATCH_THUB_P = slurm_list[i]
		i += 1
		self.SBATCH_THUB_C = slurm_list[i]
		i += 1
		self.SBATCH_THUB_MPC = slurm_list[i]
		i += 1

	def _get_SRAs(self, DIR):
		status, sdout = commands.getstatusoutput("find %s -not -path '*/\.*' -type f -name '*.sra'" % DIR)
		if status == 0:
			return_list = sorted(sdout.split("\n"))

			if return_list[0] == "":
				sys.exit("ERROR: no sample files found in given directory: %s" % DIR)
			else:
				return return_list

		else:
			sys.exit("ERROR: %s" % sdout)

	def _get_FQs(self, DIR):
		status, sdout = commands.getstatusoutput("find %s -not -path '*/\.*' -type f -name '*%s*'" % (DIR, self.d["FASTA SUFFIX"]))
		if status == 0:
			return_list = sorted(sdout.split("\n"))

			if return_list[0] == "":
				sys.exit("ERROR: no sample files found in given directory: %s" % DIR)
			else:
				return return_list

		else:
			sys.exit("ERROR: %s" % sdout)

	def _get_BAMs(self, DIR):
		status, sdout = commands.getstatusoutput("find %s -not -path '*/\.*' -type f -name '*.sortedByCoord.out.bam'" % DIR)
		if status == 0:
			sorted_list = sorted(sdout.split("\n"))
			return_list = []

			for i in sorted_list:
				if ".bai" not in i:
					return_list.append(i)

			if return_list[0] == "":
				sys.exit("ERROR: no sample files found in given directory: %s" % DIR)
			else:
				return return_list

		else:
			sys.exit("ERROR: %s" % sdout)

	def _populate(self, DIR):

		red = "%s/RED" % DIR
		red_o = "%s/slurm_output" % red
		red_e = "%s/slurm_error" % red

		if not os.path.isdir(DIR):
			os.popen("mkdir %s" % DIR)
		if not os.path.isdir(red):
			os.popen("mkdir %s" % red)
		if not os.path.isdir(red_o):
			os.popen("mkdir %s" % red_o)
		if not os.path.isdir(red_e):
			os.popen("mkdir %s" % red_e)

		os.popen("cp -r %s %s" % (self.d["INPUT VARS"], red))
		os.popen("cp -r %s/find.py %s" % (self.d["PROCESSING DIR"], red))

		return [red, red_o, red_e]

	def pull_data(self):
		# ERROR CHECKING
		if (self.d["SRR NAMES"] == "" and self.d["FTP COMMAND"] == ""):
			sys.exit("ERROR: Need either SRR names and/or an FTP command in input_vars.")
			
		REDs = self._populate(self.d["SAMPLE DIR"])
		SLURM_DIR = REDs[0]
		SLURM_OUTPUT_DIR = REDs[1]
		SLURM_ERROR_DIR = REDs[2]

		D = slurm.dependency("ok")

		if (self.d["SRR NAMES"] != ""):
			for SRR in self.d["SRR NAMES"]:
				TIME = self.SBATCH_PULL_T
				JOB_NAME = "PULL_SRR"
				JOB_FILE = "%s/run_pull_SRR.sh" % self.d["PROCESSING DIR"]
				DEPENDENCY = D
				S_O = "%s/%s_%s" % (SLURM_OUTPUT_DIR, JOB_NAME, SRR)
				S_E = "%s/%s_%s" % (SLURM_ERROR_DIR, JOB_NAME, SRR)
				JOB_VARS = [self.d["SAMPLE DIR"], SRR]

				# time, job_name, job_file, job_vars, slurmOutput_dir, slurmError_dir, dependency_id, partition, cpu_per_task, mem_per_cpu
				cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_PULL_P, self.SBATCH_PULL_C, self.SBATCH_PULL_MPC)
				ID = slurm.submit(cmd, JOB_NAME)
				slurm.record(cmd, ID, SLURM_DIR)

			print "Done submitting SRR pull jobs!"

		if (self.d["FTP COMMAND"] != ""):
			counter = 0
			for COMMAND in self.d["FTP COMMAND"]:

				# Update for rsync 11/28
				FTP = COMMAND.split("/Data/")[1]

				TIME = self.SBATCH_PULL_T
				JOB_NAME = "PULL_FTP"
				JOB_FILE = "%s/run_pull_FTP.sh" % self.d["PROCESSING DIR"]
				DEPENDENCY = D
				S_O = "%s/%s_%i" % (SLURM_OUTPUT_DIR, JOB_NAME, counter)
				S_E = "%s/%s_%i" % (SLURM_ERROR_DIR, JOB_NAME, counter)
				JOB_VARS = [self.d["SAMPLE DIR"], FTP]

				# time, job_name, job_file, job_vars, slurmOutput_dir, slurmError_dir, dependency_id, partition, cpu_per_task, mem_per_cpu
				cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_PULL_P, self.SBATCH_PULL_C, self.SBATCH_PULL_MPC)
				ID = slurm.submit(cmd, JOB_NAME)
				slurm.record(cmd, ID, SLURM_DIR)
				counter += 1

			print "Done submitting FTP pull job!"

	def convert2fastq(self):
		REDs = self._populate(self.d["SAMPLE DIR"])
		SLURM_DIR = REDs[0]
		SLURM_OUTPUT_DIR = REDs[1]
		SLURM_ERROR_DIR = REDs[2]
		
		SRA_list = self._get_SRAs(self.d["SAMPLE DIR"])
		D = slurm.dependency("ok")
		for SRA in SRA_list:
			split_name = SRA.split("/")
			shaved_name = split_name[len(split_name)-1]

			TIME = self.SBATCH_PULL_T
			JOB_NAME = "CONVERT_2_FASTQ"
			JOB_FILE = "%s/run_SRR_to_fastq.sh" % self.d["PROCESSING DIR"]
			DEPENDENCY = D
			S_O = "%s/%s_%s" % (SLURM_OUTPUT_DIR, JOB_NAME, shaved_name)
			S_E = "%s/%s_%s" % (SLURM_ERROR_DIR, JOB_NAME, shaved_name)
			JOB_VARS = [self.d["SAMPLE DIR"], SRA]

			# time, job_name, job_file, job_vars, slurmOutput_dir, slurmError_dir, dependency_id, partition, cpu_per_task, mem_per_cpu
			cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_PULL_P, self.SBATCH_PULL_C, self.SBATCH_PULL_MPC)
			ID = slurm.submit(cmd, JOB_NAME)
			slurm.record(cmd, ID, SLURM_DIR)

	def make_custom(self):
		if self.d["CUSTOMIZE"] == "T":
			REDs = self._populate(self.d["INDEX DIR"])
			SLURM_DIR = REDs[0]
			SLURM_OUTPUT_DIR = REDs[1]
			SLURM_ERROR_DIR = REDs[2]

			# Create custom reference fasta
			TIME = self.SBATCH_CUSTOM_T
			JOB_NAME = "CUSTOMIZE_REF"
			JOB_FILE = "%s/run_STAR_prep.sh" % self.d["PROCESSING DIR"]
			JOB_VARS = [self.d["PROCESSING DIR"], self.d["REF FA"], self.d["ADD FA"], self.d["CUSTOM FA"]]
			DEPENDENCY = slurm.dependency("ok")
			S_O = "%s/%s" % (SLURM_OUTPUT_DIR, JOB_NAME)
			S_E = "%s/%s" % (SLURM_ERROR_DIR, JOB_NAME)

			# time, job_name, job_file, job_vars, slurmOutput_dir, slurmError_dir, dependency_id, partition, cpu_per_task, mem_per_cpu
			cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_CUSTOM_P, self.SBATCH_CUSTOM_C, self.SBATCH_CUSTOM_MPC)
			ID = slurm.submit(cmd, JOB_NAME)
			slurm.record(cmd, ID, SLURM_DIR)

			# Only need to change these variable to create custom annotation
			JOB_NAME = "CUSTOMIZE_ANNO"
			JOB_VARS = [self.d["PROCESSING DIR"], self.d["REF ANNO"], self.d["ADD ANNO"], self.d["CUSTOM ANNO"]]
			S_O = "%s/%s" % (SLURM_OUTPUT_DIR, JOB_NAME)
			S_E = "%s/%s" % (SLURM_ERROR_DIR, JOB_NAME)

			cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_CUSTOM_P, self.SBATCH_CUSTOM_C, self.SBATCH_CUSTOM_MPC)
			ID = slurm.submit(cmd, JOB_NAME)
			slurm.record(cmd, ID, SLURM_DIR)

			print "Done submitting customization jobs!"
		else:
			print "WARNING: You entered F for CUSTOMIZATION input variable. This option is only for custom genomes. No action has been activated."

	def make_index(self):
		REDs = self._populate(self.d["INDEX DIR"])
		SLURM_DIR = REDs[0]
		SLURM_OUTPUT_DIR = REDs[1]
		SLURM_ERROR_DIR = REDs[2]

		TIME = self.SBATCH_INDEX_T
		JOB_NAME = "STAR_INDEX"
		JOB_FILE = "%s/run_STAR_index.sh" % self.d["PROCESSING DIR"]
		JOB_VARS = [self.d["STAR MODULE"], self.d["RUN THREAD"], self.d["SJBD OVERHANG"], self.d["INDEX DIR"], self.d["USE FA"], self.d["USE ANNO"], self.d["STAR INDEX PARAMS"]]
		DEPENDENCY = slurm.dependency("ok")
		S_O = "%s/%s" % (SLURM_OUTPUT_DIR, JOB_NAME)
		S_E = "%s/%s" % (SLURM_ERROR_DIR, JOB_NAME)

		cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_INDEX_P, self.SBATCH_INDEX_C, self.SBATCH_INDEX_MPC)
		ID = slurm.submit(cmd, JOB_NAME)
		slurm.record(cmd, ID, SLURM_DIR)

		print "Done submitting index job!"

	def make_align(self):
		if not os.path.isdir(self.d["DATA DIR"]):
			os.popen("mkdir %s" % self.d["DATA DIR"])

		REDs = self._populate(self.d["ALIGN DIR"])
		SLURM_DIR = REDs[0]
		SLURM_OUTPUT_DIR = REDs[1]
		SLURM_ERROR_DIR = REDs[2]

		TIME = self.SBATCH_ALIGN_T
		JOB_NAME = "STAR_ALIGN"
		DEPENDENCY = slurm.dependency("ok")
		
		FQs = self._get_FQs(self.d["SAMPLE DIR"])

		# For single end data
		if self.d["SINGLE PAIR"] == "S":
			for file in FQs:
				split_name = file.split("/")

				shaved_name = split_name[len(split_name)-1]
				# shaved_name = "%s_%s" % (split_name[len(split_name)-2], split_name[len(split_name)-1])
				shaved_name = shaved_name.split(self.d["FASTA SUFFIX"])[0]

				if self.d["PAIRED SUFFIX"] != "":
					shaved_name = shaved_name.replace(self.d["PAIRED SUFFIX"], "_SE")

				bam_file = "%s/%s." % (self.d["ALIGN DIR"], shaved_name)

				JOB_FILE = "%s/run_STAR_align_S.sh" % self.d["PROCESSING DIR"]
				JOB_VARS = [self.d["STAR MODULE"], self.d["INDEX DIR"], self.d["RUN THREAD"], file, bam_file, self.d["ZIPPED"], self.d["STAR ALIGN PARAMS"]]
				S_O = "%s/%s_%s" % (SLURM_OUTPUT_DIR, JOB_NAME, shaved_name)
				S_E = "%s/%s_%s" % (SLURM_ERROR_DIR, JOB_NAME, shaved_name)

				cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_ALIGN_P, self.SBATCH_ALIGN_C, self.SBATCH_ALIGN_MPC)
				ID = slurm.submit(cmd, JOB_NAME)
				slurm.record(cmd, ID, SLURM_DIR)

		# For paired end data
		elif self.d["SINGLE PAIR"] == "P":
			for i in range(0, len(FQs), 2):
				file_R1 = FQs[i]
				file_R2 = FQs[i+1]

				split_name = file_R1.split("/")
				bam_file = split_name[len(split_name)-1]
				bam_file = bam_file.split(self.d["FASTA SUFFIX"])[0]
				shaved_name = bam_file.replace(self.d["PAIRED SUFFIX"], "_PE")

				bam_file = "%s/%s." % (self.d["ALIGN DIR"], shaved_name)

				JOB_FILE = "%s/run_STAR_align_P.sh" % self.d["PROCESSING DIR"]
				JOB_VARS = [self.d["STAR MODULE"], self.d["INDEX DIR"], self.d["RUN THREAD"], file_R1, file_R2, bam_file, self.d["ZIPPED"], self.d["STAR ALIGN PARAMS"]]
				S_O = "%s/%s_%s" % (SLURM_OUTPUT_DIR, JOB_NAME, shaved_name)
				S_E = "%s/%s_%s" % (SLURM_ERROR_DIR, JOB_NAME, shaved_name)

				cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_ALIGN_P, self.SBATCH_ALIGN_C, self.SBATCH_ALIGN_MPC)
				ID = slurm.submit(cmd, JOB_NAME)
				slurm.record(cmd, ID, SLURM_DIR)

		print "Done submitting alignment jobs!"

	####################################################################################
	# POST PROCESSING FUNCTIONS
	####################################################################################

	# Runs feature counts on alignment output
	def make_feature(self):
		if not os.path.isdir(self.d["DATA DIR"]):
			os.popen("mkdir %s" % self.d["DATA DIR"])

		REDs = self._populate(self.d["FEATURECOUNT DIR"])
		SLURM_DIR = REDs[0]
		SLURM_OUTPUT_DIR = REDs[1]
		SLURM_ERROR_DIR = REDs[2]

		TIME = self.SBATCH_FC_T
		JOB_NAME = "FEATURE_COUNT"
		JOB_FILE = "%s/run_FC.sh" % self.d["PROCESSING DIR"]
		DEPENDENCY = slurm.dependency("ok")

		# Check if paired end data
		PAIRED = ""
		if self.d["SINGLE PAIR"] == "P":
			PAIRED = "-p"

		align_files = self._get_BAMs(self.d["ALIGN DIR"])
		ID_list = ""
		for file_name in align_files:
			split_name = file_name.split("/")
			shaved_name = split_name[len(split_name)-1]
			parsed_name = "%s.fcounts.txt" % shaved_name
			JOB_VARS = [self.d["SUBREAD MODULE"], self.d["USE ANNO"], "%s/%s" % (self.d["FEATURECOUNT DIR"], parsed_name), file_name, PAIRED, self.d["FC PARAMS"]]
			S_O = "%s/%s_%s" % (SLURM_OUTPUT_DIR, JOB_NAME, shaved_name)
			S_E = "%s/%s_%s" % (SLURM_ERROR_DIR, JOB_NAME, shaved_name)

			cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_FC_P, self.SBATCH_FC_C, self.SBATCH_FC_MPC)
			ID = slurm.submit(cmd, JOB_NAME)
			slurm.record(cmd, ID, SLURM_DIR)
			ID_list += "%s:" % ID

		TIME = "00:30:00"
		JOB_NAME = "FC_MATRIX"
		JOB_FILE = "%s/run_feature_matrix.sh" % self.d["PROCESSING DIR"]
		DEPENDENCY = [ID_list[:len(ID_list)-1], "ok"]

		JOB_VARS = [self.d["PROCESSING DIR"], self.d["FEATURECOUNT DIR"]]
		S_O = "%s/%s" % (SLURM_OUTPUT_DIR, JOB_NAME)
		S_E = "%s/%s" % (SLURM_ERROR_DIR, JOB_NAME)

		cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_FC_P, self.SBATCH_FC_C, self.SBATCH_FC_MPC)
		ID = slurm.submit(cmd, JOB_NAME)
		slurm.record(cmd, ID, SLURM_DIR)

		print "Done submitting feature count jobs!"

	# Runs feature counts on unparsed alignment output
	def make_mpileup(self):
		if not os.path.isdir(self.d["DATA DIR"]):
			os.popen("mkdir %s" % self.d["DATA DIR"])

		REDs = self._populate(self.d["RAW MP DIR"])
		SLURM_DIR_RAW = REDs[0]
		SLURM_OUTPUT_DIR_RAW = REDs[1]
		SLURM_ERROR_DIR_RAW = REDs[2]

		REDs = self._populate(self.d["MP DIR"])
		SLURM_DIR_PARSED = REDs[0]
		SLURM_OUTPUT_DIR_PARSED = REDs[1]
		SLURM_ERROR_DIR_PARSED = REDs[2]

		D = slurm.dependency("ok")

		align_files = self._get_BAMs(self.d["ALIGN DIR"])

		counter = 0

		for file_name in align_files:

			split_name = file_name.split("/")
			shaved_name = split_name[len(split_name)-1]

			FILE_D = D

			if not os.path.isfile("%s.bai" % file_name):
				# index submit command
				TIME = self.SBATCH_MP_T
				JOB_NAME = "SAMTOOLS_INDEX"
				JOB_FILE = "%s/run_samtools_index.sh" % self.d["PROCESSING DIR"]

				DEPENDENCY = D
				
				S_O = "%s/%s_%i" % (SLURM_OUTPUT_DIR_RAW, JOB_NAME, counter)
				S_E = "%s/%s_%i" % (SLURM_ERROR_DIR_RAW, JOB_NAME, counter)
				JOB_VARS = [self.d["SAMTOOLS MODULE"], file_name]

				cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_MP_P, self.SBATCH_MP_C, self.SBATCH_MP_MPC)
				ID = slurm.submit(cmd, JOB_NAME)
				slurm.record(cmd, ID, SLURM_DIR_RAW)

				FILE_D = [ID, "ok"]
				counter += 1

			file = open(self.d["AMPLICONS"], "r")
			for line in file:
				line = line.replace("\n", "")
				data = line.split("\t")
				chrom = data[0]
				start = int(data[1])
				end = int(data[2])
				amp_name = data[3]

				output_name = "%s_%s" % (shaved_name, amp_name)
				
				# mpileup submit command
				TIME = self.SBATCH_MP_T
				JOB_NAME = "MPILEUP_RAW"
				JOB_FILE = "%s/run_MP.sh" % self.d["PROCESSING DIR"]

				DEPENDENCY = FILE_D
				
				S_O = "%s/%s_%s" % (SLURM_OUTPUT_DIR_RAW, JOB_NAME, output_name)
				S_E = "%s/%s_%s" % (SLURM_ERROR_DIR_RAW, JOB_NAME, output_name)
				JOB_VARS = [self.d["SAMTOOLS MODULE"], self.d["USE FA"], file_name, "%s/%s.txt" % (self.d["RAW MP DIR"], output_name), chrom, start, end, self.d["MP PARAMS"]]

				cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_MP_P, self.SBATCH_MP_C, self.SBATCH_MP_MPC)
				ID = slurm.submit(cmd, JOB_NAME)
				slurm.record(cmd, ID, SLURM_DIR_RAW)

				DEPENDENCY = [ID, "ok"]

				# Parse mpileup in python parser command
				JOB_NAME = "MPILEUP_PARSED"
				JOB_FILE = "%s/run_parser.sh" % self.d["PROCESSING DIR"]
				JOB_VARS = [self.d["PROCESSING DIR"], "%s/%s.txt" % (self.d["RAW MP DIR"], output_name), "%s/%s.txt" % (self.d["MP DIR"], output_name)]
				S_O = "%s/%s_%s" % (SLURM_OUTPUT_DIR_PARSED, JOB_NAME, output_name)
				S_E = "%s/%s_%s" % (SLURM_ERROR_DIR_PARSED, JOB_NAME, output_name)

				cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_MP_P, self.SBATCH_MP_C, self.SBATCH_MP_MPC)
				ID = slurm.submit(cmd, JOB_NAME)
				slurm.record(cmd, ID, SLURM_DIR_PARSED)

			file.close()

		print "Done submitting mpileup jobs!"

	def redo_mpileup(self):
		if not os.path.isdir(self.d["DATA DIR"]):
			os.popen("mkdir %s" % self.d["DATA DIR"])

		REDs = self._populate(self.d["RAW MP DIR"])
		SLURM_DIR_RAW = REDs[0]
		SLURM_OUTPUT_DIR_RAW = REDs[1]
		SLURM_ERROR_DIR_RAW = REDs[2]

		REDs = self._populate(self.d["MP DIR"])
		SLURM_DIR_PARSED = REDs[0]
		SLURM_OUTPUT_DIR_PARSED = REDs[1]
		SLURM_ERROR_DIR_PARSED = REDs[2]

		D = slurm.dependency("any")

		file = open("./user_inputs/pile_specific.txt", "r")
		for line in file:
			line = line.replace("\n", "")
			data = line.split("\t")

			shaved_name = data[0]
			amp_name = data[1]

			status, sdout = commands.getstatusoutput("grep '%s' %s" % (amp_name, self.d["AMPLICONS"]))
			sdout = sdout.replace("\n", "")
			sdout = sdout.replace("\r", "")
			amp_info = sdout.split("\t")
			chrom = amp_info[0]
			start = amp_info[1]
			end = amp_info[2]

			file_name = "%s/%s" % (self.d["ALIGN DIR"], shaved_name)
			output_name = "%s_%s" % (shaved_name, amp_name)
			
			# mpileup submit command
			TIME = self.SBATCH_MP_T
			DEPENDENCY = D
			JOB_NAME = "MPILEUP_RAW"
			JOB_FILE = "%s/run_MP.sh" % self.d["PROCESSING DIR"]
			
			S_O = "%s/%s_%s" % (SLURM_OUTPUT_DIR_RAW, JOB_NAME, output_name)
			S_E = "%s/%s_%s" % (SLURM_ERROR_DIR_RAW, JOB_NAME, output_name)
			JOB_VARS = [self.d["SAMTOOLS MODULE"], self.d["USE FA"], file_name, "%s/%s.txt" % (self.d["RAW MP DIR"], output_name), chrom, start, end, self.d["MP PARAMS"]]

			cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_MP_P, self.SBATCH_MP_C, self.SBATCH_MP_MPC)
			ID = slurm.submit(cmd, JOB_NAME)
			DEPENDENCY = [ID, "ok"]
			slurm.record(cmd, ID, SLURM_DIR_RAW)

			# Parse mpileup in python parser command
			JOB_NAME = "MPILEUP_PARSED"
			JOB_FILE = "%s/run_parser.sh" % self.d["PROCESSING DIR"]
			JOB_VARS = [self.d["PROCESSING DIR"], "%s/%s.txt" % (self.d["RAW MP DIR"], output_name), "%s/%s.txt" % (self.d["MP DIR"], output_name)]
			S_O = "%s/%s_%s" % (SLURM_OUTPUT_DIR_PARSED, JOB_NAME, output_name)
			S_E = "%s/%s_%s" % (SLURM_ERROR_DIR_PARSED, JOB_NAME, output_name)

			cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_MP_P, self.SBATCH_MP_C, self.SBATCH_MP_MPC)
			ID = slurm.submit(cmd, JOB_NAME)
			slurm.record(cmd, ID, SLURM_DIR_PARSED)

		file.close()

		print "Done submitting redo mpileup jobs!"

	def make_totals(self):
		if not os.path.isdir(self.d["DATA DIR"]):
			os.popen("mkdir %s" % self.d["DATA DIR"])

		REDs = self._populate(self.d["TOTALS DIR"])
		SLURM_DIR = REDs[0]
		SLURM_OUTPUT_DIR = REDs[1]
		SLURM_ERROR_DIR = REDs[2]

		D = slurm.dependency("ok")

		align_files = self._get_BAMs(self.d["ALIGN DIR"])

		for file_name in align_files:

			split_name = file_name.split("/")
			shaved_name = split_name[len(split_name)-1]

			TIME = self.SBATCH_MP_T
			DEPENDENCY = D
			JOB_NAME = "SAMTOOLS_VIEW"
			JOB_FILE = "%s/run_view.sh" % self.d["PROCESSING DIR"]
			
			S_O = "%s/%s_%s" % (SLURM_OUTPUT_DIR, JOB_NAME, shaved_name)
			S_E = "%s/%s_%s" % (SLURM_ERROR_DIR, JOB_NAME, shaved_name)
			JOB_VARS = [self.d["SAMTOOLS MODULE"], self.d["PROCESSING DIR"], file_name, self.d["AMPLICONS"], "%s/%s.txt" % (self.d["TOTALS DIR"], shaved_name)]

			cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_MP_P, self.SBATCH_MP_C, self.SBATCH_MP_MPC)
			ID = slurm.submit(cmd, JOB_NAME)
			slurm.record(cmd, ID, SLURM_DIR)

		print "Done submitting samtools view jobs!"

	def make_multicov(self):

		if not os.path.isdir(self.d["DATA DIR"]):
			os.popen("mkdir %s" % self.d["DATA DIR"])

		REDs = self._populate(self.d["MULTICOV DIR"])
		SLURM_DIR = REDs[0]
		SLURM_OUTPUT_DIR = REDs[1]
		SLURM_ERROR_DIR = REDs[2]

		BAMs = self._get_BAMs(self.d["ALIGN DIR"])

		DEPENDENCY = slurm.dependency("ok")
		
		for bam in BAMs:

			f_list = [("1E-9", "1E_9"), ("0.05", "0.05"), ("0.1", "0.1"), ("'1E-9 -p'", "1E_9_PON"), ("'0.05 -p'", "0.05_PON"), ("'0.1 -p'", "0.1_PON")]

			for f in f_list:
				split_name = bam.split("/")
				shaved_name = split_name[len(split_name)-1]
				shaved_name = shaved_name.split(".Aligned")[0]
				shaved_name += "_%s" % f[1]
				output = "%s/%s.txt" % (self.d["MULTICOV DIR"], shaved_name)

				TIME = "01:00:00"
				JOB_NAME = "MULTICOV"
				JOB_FILE = "%s/run_multicov.sh" % self.d["PROCESSING DIR"]
				JOB_VARS = [f[0], bam, self.d["AMPLICONS"], output]
				S_O = "%s/%s" % (SLURM_OUTPUT_DIR, shaved_name)
				S_E = "%s/%s" % (SLURM_ERROR_DIR, shaved_name)
				PARTITION = "gc"
				CPU = "default"
				MEM = "default"

				cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, PARTITION, CPU, MEM)
				ID = slurm.submit(cmd, JOB_NAME)

				slurm.record(cmd, ID, SLURM_DIR)

		print "Done submitting bedtools multicov view jobs!"

	def make_fastqc(self):
		if not os.path.isdir(self.d["DATA DIR"]):
			os.popen("mkdir %s" % self.d["DATA DIR"])

		REDs = self._populate(self.d["FASTQC DIR"])
		SLURM_DIR = REDs[0]
		SLURM_OUTPUT_DIR = REDs[1]
		SLURM_ERROR_DIR = REDs[2]

		TIME = self.SBATCH_FQC_T
		JOB_NAME = "FASTQC"
		JOB_FILE = "%s/run_FQC.sh" % self.d["PROCESSING DIR"]
		DEPENDENCY = slurm.dependency("ok")
		
		FQs = self._get_FQs(self.d["SAMPLE DIR"])

		for file in FQs:

			split_name = file.split("/")
			shaved_name = split_name[len(split_name)-1]

			JOB_VARS = [self.d["FASTQC DIR"], file]
			S_O = "%s/%s_%s" % (SLURM_OUTPUT_DIR, JOB_NAME, shaved_name)
			S_E = "%s/%s_%s" % (SLURM_ERROR_DIR, JOB_NAME, shaved_name)

			cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_FQC_P, self.SBATCH_FQC_C, self.SBATCH_FQC_MPC)
			ID = slurm.submit(cmd, JOB_NAME)
			slurm.record(cmd, ID, SLURM_DIR)

		print "Done submitting FQC jobs!"

	def make_rseqc(self):
		if not os.path.isdir(self.d["DATA DIR"]):
			os.popen("mkdir %s" % self.d["DATA DIR"])

		REDs = self._populate(self.d["RSEQC DIR"])
		SLURM_DIR = REDs[0]
		SLURM_OUTPUT_DIR = REDs[1]
		SLURM_ERROR_DIR = REDs[2]

		TIME = self.SBATCH_RQC_T
		DEPENDENCY = slurm.dependency("ok")
		
		BAMs = self._get_BAMs(self.d["ALIGN DIR"])

		input_string = ""

		ID_list = ""
		counter = 0
		for file in BAMs:
			if not os.path.isfile("%s.bai" % file):
				# index submit command
				TIME = self.SBATCH_MP_T
				JOB_NAME = "SAMTOOLS_INDEX"
				JOB_FILE = "%s/run_samtools_index.sh" % self.d["PROCESSING DIR"]
				
				S_O = "%s/%s_%i" % (SLURM_OUTPUT_DIR, JOB_NAME, counter)
				S_E = "%s/%s_%i" % (SLURM_ERROR_DIR, JOB_NAME, counter)
				JOB_VARS = [self.d["SAMTOOLS MODULE"], file]

				cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_MP_P, self.SBATCH_MP_C, self.SBATCH_MP_MPC)
				ID = slurm.submit(cmd, JOB_NAME)
				slurm.record(cmd, ID, SLURM_DIR)
				counter += 1

				DEPENDENCY = [ID, "ok"]

			input_string += "%s," % file

			split_name = file.split("/")
			output_name = split_name[len(split_name)-1]

			JOB_NAME = "RSEQC"
			JOB_FILE = "%s/run_RQC_bySample.sh" % self.d["PROCESSING DIR"]
			JOB_VARS = ["%s/%s" % (self.d["RSEQC DIR"], output_name), file, self.d["REF BED"]]
			S_O = "%s/%s_%s" % (SLURM_OUTPUT_DIR, JOB_NAME, output_name)
			S_E = "%s/%s_%s" % (SLURM_ERROR_DIR, JOB_NAME, output_name)

			cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_RQC_P, self.SBATCH_RQC_C, self.SBATCH_RQC_MPC)
			ID = slurm.submit(cmd, JOB_NAME)
			slurm.record(cmd, ID, SLURM_DIR)
			ID_list += "%s:" % ID

		input_string = input_string[:len(input_string)-1]

		JOB_NAME = "RSEQC_ALL"
		JOB_FILE = "%s/run_RQC_bySet.sh" % self.d["PROCESSING DIR"]
		JOB_VARS = ["%s/ALL" % self.d["RSEQC DIR"], input_string, self.d["REF BED"]]
		S_O = "%s/%s" % (SLURM_OUTPUT_DIR, JOB_NAME)
		S_E = "%s/%s" % (SLURM_ERROR_DIR, JOB_NAME)
		DEPENDENCY = [ID_list[:len(ID_list)-1], "ok"]

		cmd = slurm.make_cmd(TIME, JOB_NAME, JOB_FILE, JOB_VARS, S_O, S_E, DEPENDENCY, self.SBATCH_RQC_P, self.SBATCH_RQC_C, self.SBATCH_RQC_MPC)
		ID = slurm.submit(cmd, JOB_NAME)
		slurm.record(cmd, ID, SLURM_DIR)

		print "Done submitting RSEQC jobs!"

	def make_trackhub(self):
		print "Trackhub not implemented yet..."





