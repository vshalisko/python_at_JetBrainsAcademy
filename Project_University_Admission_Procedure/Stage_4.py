file = open("../applicant_list.txt", "r")
applicants = file.readlines()
file.close()

deps = ["Biotech", "Chemistry", "Engineering", "Mathematics", "Physics"]

M = int(input())

applicant_db = []
for line in applicants:
    line = line[:-1]
    firstname, lastname, GPA, OP1, OP2, OP3 = line.split(" ")
    applicant = firstname + " " + lastname
    applicant_db.append([applicant, float(GPA), OP1, OP2, OP3])

def remove_item(list_to_process, to_remove):
    for i in range(len(list_to_process)):
        if list_to_process[i][0] == to_remove:
            #print("Removing:", i)
            list_to_process.pop(i)
            break
    return list_to_process

#print(len(applicant_db))

applicants_by_dep = {}
for dep in deps:
    filtered_applicants = list(filter(lambda x: x[2] == dep, applicant_db))
    sorted_applicants = sorted(filtered_applicants, key=lambda x: (-x[1], x[0]))
    applicants_selection = []
    for i in range(M):
        if len(sorted_applicants) > 0:
            applicants_selection.append(sorted_applicants.pop(0))
            remove_item(applicant_db, applicants_selection[-1][0])
    applicants_by_dep[dep] = applicants_selection

#print(len(applicant_db))

for dep in deps:
    filtered_applicants = list(filter(lambda x: x[3] == dep, applicant_db))
    sorted_applicants = sorted(filtered_applicants, key=lambda x: (-x[1], x[0]))
    applicants_selection = applicants_by_dep[dep]
    for i in range(M - len(applicants_selection)):
        if len(sorted_applicants) > 0:
            applicants_selection.append(sorted_applicants.pop(0))
            remove_item(applicant_db, applicants_selection[-1][0])
    applicants_by_dep[dep] = applicants_selection

for dep in deps:
    filtered_applicants = list(filter(lambda x: x[4] == dep, applicant_db))
    sorted_applicants = sorted(filtered_applicants, key=lambda x: (-x[1], x[0]))
    applicants_selection = applicants_by_dep[dep]
    for i in range(M - len(applicants_selection)):
        if len(sorted_applicants) > 0:
            applicants_selection.append(sorted_applicants.pop(0))
            remove_item(applicant_db, applicants_selection[-1][0])
    applicants_by_dep[dep] = applicants_selection

for dep in deps:
    print(dep)
    sorted_applicants = applicants_by_dep[dep]
    sorted_applicants = sorted(sorted_applicants, key=lambda x: (-x[1], x[0]))
    for i in range(len(sorted_applicants)):
        print("{} {}".format(sorted_applicants[i][0], sorted_applicants[i][1]))
    print()
