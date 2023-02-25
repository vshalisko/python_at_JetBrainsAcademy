
import string
import gzip

def read_gzip(file_name):
    #print(file_name)
    with gzip.open(file1, 'rt') as f:
        #print(f)
        #file_content = f.read().splitlines()
        file_content = f.read().splitlines()
        #print(file_content)
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
    n_reads = 0
    length_sum = 0
    repeats_sum = 0
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
                n_reads += 1

            if lengths.get(read_length) == None:
                lengths[read_length] = 1
            else:
                lengths[read_length] += 1

            if reads_dict.get(stripped_sequence) == None:
                reads_dict[stripped_sequence] = 1
            else:
                reads_dict[stripped_sequence] += 1
                repeats_sum += 1

    length_average = int(round(length_sum / reads_count, 0))
    proportion_cg_average = round(proportion_cg_sum / reads_count, 2)
    proportion_ns_average = round(proportion_ns_sum / reads_count, 2)
    files_data.append({
        'reads_count': reads_count,
        'length_average': length_average,
        'repeats_sum': repeats_sum,
        'n_reads': n_reads,
        'proportion_cg_average': proportion_cg_average,
        'proportion_ns_average': proportion_ns_average
    })

## input reading
file1 = str(input())
file2 = str(input())
file3 = str(input())

files_data = []

## Gunzipping and quality scores
quality_scores(read_gzip(file1))
quality_scores(read_gzip(file2))
quality_scores(read_gzip(file3))

best = files_data[0]
for data in files_data:
    if data['repeats_sum'] < best['repeats_sum'] and data['n_reads'] < best['n_reads']:
        best = data

## output
print("Reads in the file = {}:".format(best["reads_count"]))
print("Reads sequence average length = {}".format(best["length_average"]))
print("\nRepeats = {}".format(best["repeats_sum"]))
print("Reads with Ns = {}".format(best["n_reads"]))
print("\nGC content average = {}%".format(best["proportion_cg_average"]))
print("Ns per read sequence = {}%".format(best["proportion_ns_average"]))
