
import string
import gzip
#import os
#import io
#import math

#print(os.path())

#fastq_file = str(input())
#fastq = open(fastq_file, "r")
#data = fastq.readlines()
#fastq.close()

def read_gzip(file_name):
    print(file_name)
    with gzip.open(file1, 'rb') as f:
        print(f)
        file_content = f.read().splitlines()
        print(file_content)
    return file_content

def read_fastq(file_name):
    fastq = open(file1, "r")
    data = fastq.readlines()
    fastq.close()
    return data

def quality_scores(data):
    lengths = dict()
    reads_dict = dict()
    reads_count = 0
    reads_with_ns_count = 0
    length_sum = 0
    repits_sum = 0
    proportion_cg_sum = 0
    proportion_ns_sum = 0
    for i in range(0, len(data)):
        if i % 4 == 0 or i == 0:
            reads_count += 1
            stripped_sequence = data[i + 1].strip()

            count_c = stripped_sequence.upper().count('C')
            count_g = stripped_sequence.upper().count('G')
            count_n = stripped_sequence.upper().count('N')

            read_length = len(stripped_sequence)
            proportion_cg = 100 * (count_c + count_g) / read_length
            length_sum += read_length
            proportion_cg_sum += proportion_cg
            proportion_ns = 100 * count_n / read_length
            proportion_ns_sum += proportion_ns

            if count_n != None and count_n > 0:
                reads_with_ns_count += 1

            if lengths.get(read_length) == None:
                lengths[read_length] = 1
            else:
                lengths[read_length] += 1

            if reads_dict.get(stripped_sequence) == None:
                reads_dict[stripped_sequence] = 1
            else:
                reads_dict[stripped_sequence] += 1
                repits_sum += 1

    length_average = int(round(length_sum / reads_count, 0))
    proportion_cg_average = round(proportion_cg_sum / reads_count, 2)
    proportion_ns_average = round(proportion_ns_sum / reads_count, 2)
    return reads_count, length_average, repits_sum, reads_with_ns_count, proportion_cg_average, proportion_ns_average


## input reading
file1 = str(input())
file2 = str(input())
file3 = str(input())

## gunzipping - FAILURE sithe first test data
#a, b, c, d, e, f = quality_scores(read_fastq(file1))
a1, b1, c1, d1, e1, f1 = quality_scores(read_gzip(file1))
a2, b2, c2, d2, e2, f2 = quality_scores(read_gzip(file2))
a3, b3, c3, d3, e3, f3 = quality_scores(read_gzip(file3))


## bert score selector
index1 = f1 + c1
index2 = f2 + c2
index3 = f3 + c3

a, b, c, d, e, f = a1, b1, c1, d1, e1, f1

## output
print("Reads in the file = {}:".format(a))
print("Reads sequence average length = {}".format(b))
print("\nRepeats = {}".format(c))
print("Reads with Ns = {}".format(d))
print("\nGC content average = {}%".format(e))
print("Ns per read sequence = {}%".format(f))

