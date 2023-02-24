import string
import os
#import math

#print(os.path())

fastq_file = str(input())
fastq = open(fastq_file, "r")
data = fastq.readlines()
fastq.close()

lengths = dict()
reads_dict = dict()
reads_count = 0
length_sum = 0
repits_sum = 0
proportion_cg_sum = 0

for i in range(0, len(data)):
    if i % 4 == 0 or i == 0:
        reads_count += 1
        stripped_sequence = data[i + 1].strip()

        count_c = stripped_sequence.upper().count('C')
        count_g = stripped_sequence.upper().count('G')

        read_length = len(stripped_sequence)
        proportion_cg = 100 * (count_c + count_g) / read_length

        length_sum += read_length
        proportion_cg_sum += proportion_cg
        if lengths.get(read_length) == None:
            lengths[read_length] = 1
        else:
            lengths[read_length] += 1

        if reads_dict.get(stripped_sequence) == None:
            reads_dict[stripped_sequence] = 1
        else:
            reads_dict[stripped_sequence] += 1
            repits_sum += 1
            #print(data[i+1].strip())

print("Reads in the file = {}:".format(reads_count))
#print(lengths)

#for j in lengths:
    #print("      with length {} = {}".format(j, lengths[j]))
    #length_sum += int(j) * int(lengths[j])

length_average = int(round(length_sum / reads_count, 0))
print("\nReads sequence average length = {}".format(length_average))
print("\nRepeats = {}".format(repits_sum))
proportion_cg_average = round(proportion_cg_sum / reads_count, 2)
print("GC content average = {}%".format(proportion_cg_average))
