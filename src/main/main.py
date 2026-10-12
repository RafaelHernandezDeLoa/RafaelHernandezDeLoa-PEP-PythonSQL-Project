import csv
import os
import sqlite3

# Resolve the resources folder relative to this file, so paths work
# no matter what directory the script is run from.
_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'resources')

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # You will implement these methods below. They just print TO-DO messages for now.
    load_and_clean_users(os.path.join(_RESOURCES_DIR, 'users.csv'))
    load_and_clean_call_logs(os.path.join(_RESOURCES_DIR, 'callLogs.csv'))
    write_user_analytics(os.path.join(_RESOURCES_DIR, 'userAnalytics.csv'))
    write_ordered_calls(os.path.join(_RESOURCES_DIR, 'orderedCalls.csv'))

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    select_from_users_and_call_logs()

    # Close the cursor and connection. main function ends here.
    cursor.close()
    conn.close()


# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.


# This function will load the users.csv file into the users table, discarding any records with incomplete data
def load_and_clean_users(file_path):
    count = 1

    with open(file_path, "r") as file:
        for line in file:
            if count == 1:
                count -= 1
                continue

            with_spaces = line.split(",")
            name = []

            for elements in with_spaces:
                name.append(elements.strip())
                if elements.strip() == "":
                    name.pop(len(name)-1)
            
            if len(name) == 2:
                cursor.execute("""
                    INSERT INTO users(firstName, lastName) VALUES (?, ?)
                """, (name[0], name[1]))

    #print("TODO: load_users")


# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
def load_and_clean_call_logs(file_path):
    count = 1

    with open(file_path, "r") as file:
        for line in file:
            if count == 1:
                count -= 1
                continue

            with_spaces = line.split(",")
            log = []

            for elems in with_spaces:
                if elems.strip() != "":
                    log.append(elems.strip())
            
            if len(log) == 5:
                cursor.execute("""
                    INSERT INTO callLogs(phoneNumber, startTime, endTime, direction, userId) VALUES (?, ?, ?, ?, ?)
                """, (log[0], log[1], log[2], log[3], log[4]))

    #print("TODO: load_call_logs")


# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.
def write_user_analytics(csv_file_path):
    cursor.execute("""
        SELECT * FROM callLogs
    """)

    logs = cursor.fetchall()

    duration = {}
    call_nums = {}

    for log in logs:
        if call_nums.has_key(log[5]) and duration.has_key(log[5]):
            call_nums[log[5]] = call_nums.get(log[5]) + 1
            duration[log[5]] += log[3] - log[2]
        else:
            call_nums.update(log[5], 1)
            duration.update(log[5], log[3] - log[2])
    
    for key in duration:
        duration[key] = duration.get(key) / call_nums[key]
    
    with open(csv_file_path, "a") as file:
        for key in duration:
            file.write(key + "," + duration[key] + "," + call_nums[key] + "\n")
        
    
    #print("TODO: write_user_analytics")


# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv
def write_ordered_calls(csv_file_path):

    print("TODO: write_ordered_calls")



# No need to touch the functions below!------------------------------------------

# This function is for debugs/validation - uncomment the function invocation in main() to see the data in the database.
def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    # new line
    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM callLogs''')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()