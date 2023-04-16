import smtplib
from email.mime.text import MIMEText


def save(students, filepath):  # punkt 5
    with open(filepath, "w") as file_object:
        for student in students:
            str = ""
            if len(student) > 4:
                str = student["email"] + "," + student["name"] + "," + student["lastName"] + "," + student[
                    "points"] + "," + student["grade"] + "," + student["gradeStatus"]
            else:
                str = student["email"] + "," + student["name"] + "," + student["lastName"] + "," + student["points"]
            file_object.write(str + "\n")


def grade(students):  # punkt 2
    for student in students:
        if len(student) == 4:
            student["gradeStatus"] = "GRADED"
            if int(student["points"]) <= 50:
                student["grade"] = "2"
            elif int(student["points"]) <= 60:
                student["grade"] = "3"
            elif int(student["points"]) <= 70:
                student["grade"] = "3.5"
            elif int(student["points"]) <= 80:
                student["grade"] = "4"
            elif int(student["points"]) <= 90:
                student["grade"] = "4.5"
            elif int(student["points"]) <= 100:
                student["grade"] = "5"


def addStudent(students):
    str = input(
        "\n\nPodaj dane studenta w formacie: 'email,imie,nazwisko,punkty,ocena(opcjonalne),statusOceny(obowiazkowe jesli podajesz ocene)':\n")
    obecny = False
    strings = str.split(",")
    email = strings[0]
    for student in students:
        if student["email"] == email:
            obecny = True
    if obecny:
        print("W systemie jest juz student o podanym emailu!")
        input("<<NACISNIJ ENTER ABY KONTYNUOWAC>>")
    else:
        if len(strings) > 4:
            student = {"email": strings[0], "name": strings[1], "lastName": strings[2], "points": strings[3],
                       "grade": strings[4], "gradeStatus": strings[5]}
            students.append(student)
        else:
            student = {"email": strings[0], "name": strings[1], "lastName": strings[2], "points": strings[3]}
            students.append(student)
        print("Student dodany")
        input("<<NACISNIJ ENTER ABY KONTYNUOWAC>>")


def deleteStudent(students):
    str = input("\n\nPodaj email studenta ktorego chcesz usunac:\n")
    obecny = False
    newStudents = list()
    for student in students:
        if student["email"] == str:
            obecny = True
        else:
            newStudents.append(student)
    if obecny:
        print("Student usuniety")
    else:
        print("Nie ma studenta o podanym emailu")
    input("<<NACISNIJ ENTER ABY KONTYNUOWAC>>")
    return newStudents


def sendMail(students):
    sender = ""
    password = ""
    for student in students:
        if student["gradeStatus"] == "GRADED":
            student["gradeStatus"] = "MAILED"
            recipients = [student["email"]]
            msg = MIMEText("Gratulacje, twoja ocena to " + student["grade"])
            msg['Subject'] = "Oceny"
            msg['From'] = ""
            msg['To'] = student["email"]
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
            smtp_server.quit()
    print("Maile zostaly wyslane")
    input("<<NACISNIJ ENTER ABY KONTYNUOWAC>>")


students = list()

filepath = "students.txt"
with open(filepath) as file_object:  # punkt 1
    for line in file_object:
        str = line.rstrip()
        print(str)
        strings = str.split(",")
        if len(strings) > 4:
            student = {"email": strings[0], "name": strings[1], "lastName": strings[2], "points": strings[3],
                       "grade": strings[4], "gradeStatus": strings[5]}
            students.append(student)
        else:
            student = {"email": strings[0], "name": strings[1], "lastName": strings[2], "points": strings[3]}
            students.append(student)

while True:
    print("Co chcesz zrobic?"
          "\n1. Automatycznie wystawic oceny"
          "\n2. Dodac nowego studenta"
          "\n3. Usunac studenta"
          "\n4. Wyslac studentom maile z ocenami")
    answer = input("Podaj odpowiedz: ")
    if answer == "1":
        grade(students)
        save(students, filepath)
    elif answer == "2":
        addStudent(students)
        save(students, filepath)
    elif answer == "3":
        students = deleteStudent(students)
        save(students, filepath)
    elif answer == "4":
        sendMail(students)
        save(students, filepath)

    print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
