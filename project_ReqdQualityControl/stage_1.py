fastq_file = str(input())
fastq = open(fastq_file, "r")
data = fastq.readlines()
fastq.close()
reads_count = 0
lengths = dict()

for i in range(0, 4):
    if (data[i] != ""):
        print(data[i].strip())
