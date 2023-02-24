import math

fastq_file = str(input())
fastq = open(fastq_file, "r")
data = fastq.readlines()
fastq.close()
reads_count = 0
lengths = dict()

for i in range(0, len(data)):
    if i % 4 == 0 or i == 0:
        ## block start
        reads_count += 1
        read_length = str(len(data[i + 1].strip()))
        if lengths.get(read_length) == None:
            lengths[read_length] = 1
        else:
            lengths[read_length] += 1
        #print(data[i+1].strip())

print("Reads in the file = {}:".format(reads_count))
#print(lengths)
length_sum = 0
for j in lengths:
    print("      with length {} = {}".format(j, lengths[j]))
    length_sum += int(j) * int(lengths[j])

length_average = int(round(length_sum / reads_count, 0))
print("\nReads sequence average length = {}".format(length_average))
