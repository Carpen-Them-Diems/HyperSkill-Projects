from collections import defaultdict

# Take user input for the cutoff number for departments
department_cutoff = int(input())

# Create containers to later populate with the data
departments = ['Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics']
dept_students = defaultdict(list)
dept_applicants = defaultdict(lambda: defaultdict(list))

# Open and read the applicant list
with open('student_data/applicant_list3.txt', 'r') as f:
    applicant_list = []
    for line in f:
        first, last, physics, chemistry, math, cs, uni, choice_1, choice_2, choice_3 = line.split()
        applicant_list.append((first, last, float(physics), float(chemistry), float(math), float(cs), float(uni),
                               choice_1, choice_2, choice_3))

# Create separate lists for each department based on the choices
for applicant in applicant_list:
    for i in range(7, 10):
        dept = applicant[i]
        if dept == 'Physics':
            score = ((applicant[2] + applicant[4]) / 2)
            if applicant[6] > score:
                score = applicant[6]
        elif dept == 'Chemistry':
            score = applicant[3]
            if applicant[6] > score:
                score = applicant[6]
        elif dept == 'Mathematics':
            score = applicant[4]
            if applicant[6] > score:
                score = applicant[6]
        elif dept == 'Engineering':
            score = ((applicant[4] + applicant[5]) / 2)
            if applicant[6] > score:
                score = applicant[6]
        elif dept == 'Biotech':
            score = ((applicant[2] + applicant[3]) / 2)
            if applicant[6] > score:
                score = applicant[6]
        dept_applicants[dept][i].append((score,) + applicant)

# Sort the lists
for dept in departments:
    for i in range(7, 10):
        dept_applicants[dept][i].sort(key=lambda x: (-x[0], x[1], x[2]))


# Assign students to their proper departments/classes while removing them from the other possible lists
def assign_students():
    accepted_students = set()
    for i in range(7, 10):
        for dept in departments:
            j = 0
            while j < len(dept_applicants[dept][i]) and len(dept_students[dept]) < department_cutoff:
                applicant = dept_applicants[dept][i][j]
                # Check if the applicant has already been accepted by another department
                if (applicant[1], applicant[2]) not in accepted_students:
                    dept_students[dept].append(applicant)
                    accepted_students.add((applicant[1], applicant[2]))
                    j += 1
                else:
                    # If the applicant has been accepted by another department, remove them from this department's list
                    dept_applicants[dept][i].remove(applicant)
            dept_students[dept].sort(key=lambda x: (-x[0], x[1], x[2]))


assign_students()

# Print student names and relevant grade
for dept, students in sorted(dept_students.items()):
    print('\n' + dept)
    with open(f'department_files/{dept}.txt', 'w') as f:
        for student in students:
            print(student[1] + ' ' + student[2] + ' ' + str(student[0]))
            f.write(student[1] + ' ' + student[2] + ' ' + str(student[0]) + '\n')


### LEFTOVER CODE FROM EARLIER STAGES OF THE PROJECT, KEEPING IT FOR POSTERITY/FUTURE USE/STUDYING/REFLECTION ###

# exam1 = float(input())
# exam2 = float(input())
# exam3 = float(input())
#
# exam_mean = (exam1 + exam2 + exam3) / 3
#
# print(exam_mean)
#
# if exam_mean >= 60.0:
#     print('Congratulations, you are accepted!')
# else:
#     print('We regret to inform you that we will not be able to offer you admission.')


# for _ in range(applicant_total):
#     first, last, gpa, first_choice, second_choice, third_choice = input().split()
#     gpa = float(gpa)
#     applicant_list.append((first, last, gpa))

# applicant_list.sort(key=lambda x: (-x[2], x[] x[0], x[1]))

# print('Successful applicants:')

# successful_applicant_list = []
#
# for i in range(applicant_cutoff):
#     print(applicant_list[i][0] + ' ' + applicant_list[i][1])

# applicant_cutoff = int(input())

# departments = {
#     'Biotech': [],
#     'Chemistry': [],
#     'Engineering': [],
#     'Mathematics': [],
#     'Physics': []
# }
#
# with open('applicant_list.txt', 'r+') as f:
#     for line in f:
#         first_name, last_name, gpa, *priorities = line.split()
#         gpa = float(gpa)
#         for i, department in enumerate(priorities):
#             departments[department].append((first_name, last_name, gpa, i))
#
# # Sort the students by GPA, name, and department choice
# for department in departments:
#     departments[department].sort(key=lambda x: (-x[2], x[3], x[0], x[1]))
#
# for _ in range(3):
#     for department in sorted(departments):
#         selected_students = departments[department][:department_cutoff]
#         print(department)
#         # for first_name, last_name, gpa in selected_students:
#         #     print(first_name + ' ' + last_name + ' ' + str(gpa))
#         # print('\n')
#         for other_department in departments:
#             departments[other_department] = [applicant for applicant in departments[other_department] if
#                                              (applicant[0], applicant[1]) not in
#                                              (selected_applicant[0], selected_applicant[1]) for selected_applicant in
#                                              selected_students]
#
# for department in sorted(departments):
#     while len(department) < department_cutoff:
#         next_best_applicant = None

# department_cutoff = int(input())
#
# with open('applicant_list.txt', 'r') as f:
#     applicant_list = []
#     for line in f:
#         first, last, gpa, choice_1, choice_2, choice_3 = line.split()
#         applicant_list.append((first, last, float(gpa), choice_1, choice_2, choice_3))
#     # print(applicant_list)
#
# # Sort the applicants by GPA (descending) and name (ascending)
# applicant_list.sort(key=lambda x: (-float(x[2]), x[0], x[1]))

# print(applicant_list)

# # Initialize the departments
# departments = ['Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics']
# dept_students = defaultdict(list)
#
#
# # Function to assign students to departments
# def assign_students(choice):
#     global applicant_list
#     print(applicant_list)
#     remaining_applicants = []
#     for i, applicant in enumerate(applicant_list):
#         dept = applicant[choice]
#         if len(dept_students[dept]) < department_cutoff:
#             dept_students[dept].append(applicant)
#         else:
#             remaining_applicants.append(applicant)
#         applicant_list = remaining_applicants
#
#
# # Assign students based on 1st choice (index [3])
# assign_students(3)
#
# # # Assign students based on 2nd choice (index [4])
# # assign_students(4)
# #
# # # Assign students based on 3rd choice (index [5])
# # assign_students(5)
#
#
# for dept, students in sorted(dept_students.items()):
#     # print(students)
#     print('\n' + dept)
#     for student in students:
#         # print(student)
#         print(student[0] + ' ' + student[1] + ' ' + str(student[2]))

# # Take user input to declare department cutoff values #########
# department_cutoff = int(input())
#
# # Open and read in the student data
# with open('applicant_list.txt', 'r') as f:
#     applicant_list = []
#     for line in f:
#         first, last, gpa, choice_1, choice_2, choice_3 = line.split()
#         applicant_list.append((first, last, float(gpa), choice_1, choice_2, choice_3))
#
# # Sort the applicants by GPA (descending) and name (ascending)
# applicant_list.sort(key=lambda x: (-float(x[2]), x[0], x[1]))
#
# # Set up the containers for the department categories, department students, and applicants
# departments = ['Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics']
# dept_students = defaultdict(list)
# dept_applicants = defaultdict(lambda: defaultdict(list))
#
# # Create separate lists for each department based on the choices
# for applicant in applicant_list:
#     for i in range(3, 6):
#         dept = applicant[i]
#         dept_applicants[dept][i].append(applicant)
#
# # Sort these lists
# for dept in departments:
#     for i in range(3, 6):
#         dept_applicants[dept][i].sort(key=lambda x: (-x[2], x[0], x[1]))
#
#
# # Function to assign students to departments and remove them from their other choices
# def assign_students():
#     for i in range(3, 6):
#         for dept in departments:
#             while dept_applicants[dept][i] and len(dept_students[dept]) < department_cutoff:
#                 applicant = dept_applicants[dept][i].pop(0)
#                 dept_students[dept].append(applicant)
#                 for other_dept in departments:
#                     for j in range(3, 6):
#                         if applicant in dept_applicants[other_dept][j]:
#                             dept_applicants[other_dept][j].remove(applicant)
#             dept_students[dept].sort(key=lambda x: (-x[2], x[0], x[1]))
#
#
# # Run function assigning the students
# assign_students()
#
# # Finally print out the results in the requested format
# for dept, students in sorted(dept_students.items()):
#     for student in students:
#         print(student[0] + ' ' + student[1] + ' ' + str(student[2]))
