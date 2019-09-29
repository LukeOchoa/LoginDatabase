import copy
import hashlib
import secrets
import sqlite3


username = ["user"]
password = ["pass"]
Failure_Message = "     Invalid choice. Try again..."
Failure_Message2 = "     Username or Password is incorrect. Try again..."


def login_screen():

    while True:
        print("     Type |login| to log into an account    ")
        print("     Type |create| to setup a new account    ")

        conditions = {"create": [2, "create"], "login": [2, "login"]}
        condition_input = input()

        if condition_input in conditions:
            break
        else:
            print(Failure_Message)
            continue

    return conditions[condition_input]


def create_user():

    decision = ["username", "password"]
    username_password = ["placeholder 1", "placeholder 2"]

    for x in range(2):
        while True:
            print(f"        What would you like your {decision[x]} to be?")
            username_password[x] = input()
            print(
                f"        You chose ({username_password[x]}), are you sure you want this {decision[x]}?, enter |yes| or |no|")
            choice = input()
            if choice.lower() == "yes":
                break
            elif choice.lower() == "no":
                continue

    print("     Successful creation!")
    print("     Returning to main menu.")

    return username_password


def hash_andor_salt(u_and_p, connection_1):
    cursor_1 = connection_1.cursor()

    cursor_1.execute("SELECT COUNT(*) FROM user")
    id_max = cursor_1.fetchone()[0] + 1

    u_and_p[0] = hashlib.sha256(u_and_p[0].encode())  # hash the username

    item = []  # generate a salt
    for i in range(5):
        item.append(secrets.randbelow(10))
    item2 = ''.join(map(str, item))  # convert the salt to text and put it in a string
    u_and_p[1] = u_and_p[1] + item2  # add the salt to the password
    u_and_p[1] = hashlib.sha256(u_and_p[1].encode())  # hash them together

    item2 = int(item2)
    u_and_p[0] = u_and_p[0].hexdigest()
    u_and_p[1] = u_and_p[1].hexdigest()

    print(type(id_max), type(u_and_p[0]), type(u_and_p[1]), type(item2))
    entities = (id_max, u_and_p[0], u_and_p[1], item2)
    cursor_1.execute('INSERT INTO user(ID, username, password, salt) VALUES(?, ?, ?, ?)', entities)
    connection_1.commit()

    return u_and_p


def user_input(x):
    input_data = []
    for a in range(x):
        input_data.append(input())

    return input_data


def validate_credentials(u, p, cursor_2):
    bool_array = {"username": False,
                  "password": False}

    cursor_2.execute("SELECT COUNT(*) FROM user")
    ID = cursor_2.fetchone()[0] + 1

    u = hashlib.sha256(u.encode()).hexdigest()

    for i in range(1, ID):
        result = cursor_2.execute("SELECT username, password, salt FROM user WHERE ID=?", (i,))

        r = result.fetchall()
        var123 = str(r[0][2])
        pp = p + var123  # add the salt to the password
        pp = hashlib.sha256(pp.encode()).hexdigest()

        if u in r[0][0] and pp in r[0][1]:
            bool_array["username"] = True
            bool_array["password"] = True

    return bool_array


def report(B_array):
    if B_array["username"] and B_array["password"]:
        print("You've logged in.")
        return True
    else:
        print(Failure_Message2)
        print(username)
        print(password)
        return False


###################################################

# BASE_DIR = os.path.dirname(os.path.abspath__file__))
# db_path = os.path.join(BASE_DIR, "")

# connection = sqlite3.connect('db.UnstableDatabase')

connection = sqlite3.connect("UnstableData.db")

cursor11 = connection.cursor()

###################################################


while True:
    conditions_value = login_screen()

    if "create" in conditions_value:
        ToHashNORSalt = create_user()
        hash_andor_salt(ToHashNORSalt, connection)
        continue

    while True:
        print("Enter your username. Then enter your password")
        user_data = user_input(conditions_value[0])

        Pass_Fail = validate_credentials(user_data[0], user_data[1], cursor11)

        result2 = report(Pass_Fail)
        if result2:
            break

        choice3 = ""
        while True:
            print("     Try again?. Enter |yes| or |no|.")
            choice3 = input()
            if choice3.lower() == "yes":
                print("is yes?")
                choice3 = True
                break
            elif choice3.lower() == "no":
                print("is no?")
                choice3 = False
                break
            else:
                print("Bad answer. Try again...")
                continue

        if choice3:
            continue
        else:
            break

    choice2 = ""
    while True:
        print("     Do you wish to go to the main menu. Enter |yes| or |no|.")
        choice2 = input()
        if choice2.lower() == "yes":
            choice2 = True
            break
        elif choice2.lower() == "no":
            choice2 = False
            break
        else:
            print("Bad answer. Try again...")
            continue

    if choice2:
        continue
    else:
        break
