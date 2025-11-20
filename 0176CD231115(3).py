import random
import datetime
import os

student_file = "student.txt"
score_file = "score.txt"
question_file = "question.txt"

logged_user = None
logged = False


def register():
    print("\n--- Registration ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    name = input("Enter full name: ")
    email = input("Enter email: ")
    branch = input("Enter branch: ")
    year = input("Enter year: ")
    contact = input("Enter contact: ")
    enroll = input("Enter enrollment no: ")

    # check if user exists
    if os.path.exists(student_file):
        with open(student_file, "r") as f:
            for line in f:
                if line.split(",")[0] == username:
                    print("User already exists!")
                    return

    with open(student_file, "a") as f:
        f.write(f"{username},{password},{name},{email},{branch},{year},{contact},{enroll}")

    print("Registration successful!")


def login():
    global logged_user, logged
    print("\n--- Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    found = False

    if os.path.exists(student_file):
        with open(student_file, "r") as f:
            for line in f:
                data = line.strip().split(",")
                if len(data) >= 2 and data[0] == username and data[1] == password:
                    logged_user = {
                        "username": data[0],
                        "password": data[1],
                        "name": data[2],
                        "email": data[3],
                        "branch": data[4],
                        "year": data[5],
                        "contact": data[6],
                        "enroll": data[7]
                    }
                    logged = True
                    found = True
                    break
    if found:
        print("Login successful! Welcome", logged_user["name"])
    else:
        print("Invalid username or password")


def show_profile():
    if not logged:
        print("Please login first!")
        return
    print("\n--- Profile ---")
    for k, v in logged_user.items():
        if k != "password":
            print(f"{k.capitalize()}: {v}")


def update_profile():
    global logged_user
    if not logged:
        print("Please login first!")
        return

    print("\n--- Update Profile ---")
    email = input(f"Email ({logged_user['email']}): ") or logged_user['email']
    branch = input(f"Branch ({logged_user['branch']}): ") or logged_user['branch']
    year = input(f"Year ({logged_user['year']}): ") or logged_user['year']
    contact = input(f"Contact ({logged_user['contact']}): ") or logged_user['contact']
    name = input(f"Name ({logged_user['name']}): ") or logged_user['name']

    # update in memory
    logged_user['email'] = email
    logged_user['branch'] = branch
    logged_user['year'] = year
    logged_user['contact'] = contact
    logged_user['name'] = name

    # update file
    lines = []
    with open(student_file, "r") as f:
        for line in f:
            data = line.strip().split(",")
            if data[0] == logged_user['username']:
                new_line = f"{logged_user['username']},{logged_user['password']},{name},{email},{branch},{year},{contact},{logged_user['enroll']}"
                lines.append(new_line)
            else:
                lines.append(line)
    with open(student_file, "w") as f:
        f.writelines(lines)

    print("Profile updated successfully!")


def load_questions(category):
    questions = []
    if not os.path.exists(question_file):
        print("Question file not found!")
        return questions

    with open(question_file, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 7 and parts[0].upper() == category.upper():
                questions.append(parts)
    random.shuffle(questions)
    return questions[:5]  # show 5 random questions


def attempt_quiz():
    if not logged:
        print("Please login first!")
        return

    print("\n--- Quiz Categories ---")
    print("1. DSA\n2. DBMS\n3. PYTHON")
    ch = input("Choose category (1/2/3): ")

    if ch == '1':
        cat = "DSA"
    elif ch == '2':
        cat = "DBMS"
    elif ch == '3':
        cat = "PYTHON"
    else:
        print("Invalid choice!")
        return

    ques = load_questions(cat)
    if not ques:
        print("No questions found for this category!")
        return

    score = 0
    total = len(ques)

    for q in ques:
        print("\nQ:", q[1])
        print("A.", q[2])
        print("B.", q[3])
        print("C.", q[4])
        print("D.", q[5])
        ans = input("Your answer (A/B/C/D): ").upper()
        if ans == q[6].upper():
            print("Correct!")
            score += 1
        else:
            print("Wrong! Correct answer:", q[6])

    print(f"\nYou scored {score}/{total}")

    with open(score_file, "a") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{logged_user['enroll']},{cat},{score}/{total},{now}")


def logout():
    global logged_user, logged
    if logged:
        print(f"Logged out: {logged_user['username']}")
        logged_user = None
        logged = False
    else:
        print("No user logged in")


def terminate():
    print("Exiting program...")
    exit()


def main():
    while True:
        print("\n===== LNCT QUIZ APP =====")
        print("1. Register")
        print("2. Login")
        print("3. Show Profile")
        print("4. Update Profile")
        print("5. Attempt Quiz")
        print("6. Logout")
        print("7. Exit")

        ch = input("Enter your choice: ")

        if ch == '1':
            register()
        elif ch == '2':
            login()
        elif ch == '3':
            show_profile()
        elif ch == '4':
            update_profile()
        elif ch == '5':
            attempt_quiz()
        elif ch == '6':
            logout()
        elif ch == '7':
            terminate()
        else:
            print("Invalid choice!")


main()
