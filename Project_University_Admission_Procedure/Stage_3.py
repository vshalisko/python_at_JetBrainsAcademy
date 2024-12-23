N = int(input())
M = int(input())

applicatnts = []
for i in range(N):
    firstname, lastname, GPA = str(input()).split(" ")
    applicant = firstname + " " + lastname
    applicatnts.append([applicant, float(GPA)])

sorted_applicants = sorted(applicatnts, key=lambda x: (-x[1], x[0]))

print("Successful applicants:")
for i in range(M):
    print("{}".format(sorted_applicants[i][0]))
