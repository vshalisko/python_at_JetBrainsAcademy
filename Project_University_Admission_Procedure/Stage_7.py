file = open("../applicant_list_7.txt", "r")
applicants = file.readlines()
file.close()

deps = ["Biotech", "Chemistry", "Engineering", "Mathematics", "Physics"]
exams = [1, 2, 3, 4, 5]

M = int(input())

applicant_db = []
for line in applicants:
    line = line[:-1]
    firstname, lastname, EPH, ECH, EMA, ECS, ESP, OP1, OP2, OP3 = line.split(" ")
    applicant = firstname + " " + lastname
    applicant_db.append([applicant,
                         max((float(ECH) + float(EPH)) / 2, float(ESP)),
                         max(float(ECH), float(ESP)),
                         max((float(ECS) + float(EMA)) / 2, float(ESP)),
                         max(float(EMA), float(ESP)),
                         max((float(EMA) + float(EPH)) / 2, float(ESP)),
                         OP1, OP2, OP3])

def remove_item(list_to_process, to_remove):
    for i in range(len(list_to_process)):
        if list_to_process[i][0] == to_remove:
            #print("Removing:", i)
            list_to_process.pop(i)
            break
    return list_to_process

applicants_by_dep = {}

def update_dep_selection(department_id, selected, priority, limit):
    filtered_applicants = list(filter(lambda x: x[priority] == deps[department_id], applicant_db))
    exam_column = exams[department_id]
    sorted_applicants = sorted(filtered_applicants, key=lambda x: (-x[exam_column], x[0]))
    applicants_selection = selected
    for i in range(limit - len(selected)):
        if len(sorted_applicants) > 0:
            applicants_selection.append(sorted_applicants.pop(0))
            remove_item(applicant_db, applicants_selection[-1][0])
    return applicants_selection

for dep_id in range(len(deps)):
    dep = deps[dep_id]
    applicants_by_dep[dep] = []
    applicants_by_dep[dep] = update_dep_selection(dep_id,
                                                  applicants_by_dep[dep],
                                                  6, M)

for dep_id in range(len(deps)):
    dep = deps[dep_id]
    applicants_by_dep[dep] = update_dep_selection(dep_id,
                                                  applicants_by_dep[dep],
                                                  7, M)

for dep_id in range(len(deps)):
    dep = deps[dep_id]
    applicants_by_dep[dep] = update_dep_selection(dep_id,
                                                  applicants_by_dep[dep],
                                                  8, M)

#for dep_id in range(len(deps)):
#    dep = deps[dep_id]
#    exam_column = exams[dep_id]
#    print(dep)
#    sorted_applicants = applicants_by_dep[dep]
#    sorted_applicants = sorted(sorted_applicants, key=lambda x: (-x[exam_column], x[0]))
#    for i in range(len(sorted_applicants)):
#        print("{} {}".format(sorted_applicants[i][0], sorted_applicants[i][exam_column]))
#    print()

for dep_id in range(len(deps)):
    dep = deps[dep_id]
    exam_column = exams[dep_id]
    file_name = dep + ".txt"
    file = open(file_name, 'w', encoding='utf-8')
    sorted_applicants = applicants_by_dep[dep]
    sorted_applicants = sorted(sorted_applicants, key=lambda x: (-x[exam_column], x[0]))
    for i in range(len(sorted_applicants)):
        file.write(str(sorted_applicants[i][0]) + " " + str(sorted_applicants[i][exam_column]) + "\n")
    file.close()
