import string
#import math

fastq_file = str(input())
fastq = open(fastq_file, "r")
data = fastq.readlines()
fastq.close()

lengths = dict()
reads_count = 0
length_sum = 0
proportion_cg_sum = 0

for i in range(0, len(data)):
    if i % 4 == 0 or i == 0:
        reads_count += 1
        stripped_sequence = data[i + 1].strip()

        count_c = stripped_sequence.upper().count('C')
        count_g = stripped_sequence.upper().count('G')
        #count_n = stripped_sequence.upper().count('N')
        #count_a = stripped_sequence.upper().count('A')
        #count_t = stripped_sequence.upper().count('T')

        read_length = len(stripped_sequence)
        proportion_cg = 100 * (count_c + count_g) / read_length

        length_sum += read_length
        proportion_cg_sum += proportion_cg
        if lengths.get(read_length) == None:
            lengths[read_length] = 1
        else:
            lengths[read_length] += 1
        #print(data[i+1].strip())

print("Reads in the file = {}:".format(reads_count))
#print(lengths)

#for j in lengths:
    #print("      with length {} = {}".format(j, lengths[j]))
    #length_sum += int(j) * int(lengths[j])

length_average = int(round(length_sum / reads_count, 0))
print("\nReads sequence average length = {}".format(length_average))
proportion_cg_average = round(proportion_cg_sum / reads_count, 2)
print("GC content average = {}%".format(proportion_cg_average))
