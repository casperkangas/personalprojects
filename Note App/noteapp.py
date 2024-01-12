import os
import datetime
import logging
import hashlib

SCRIPT_DIR = os.path.dirname(__file__)
LOGS_FOLDER = os.path.join(SCRIPT_DIR, "logs")
NOTES_FOLDER = os.path.join(SCRIPT_DIR, "notes")
USERS_FILE = os.path.join(SCRIPT_DIR, "users.txt")
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "verystrongpassword"

# Ensure the logs, notes, and users folders exist
os.makedirs(LOGS_FOLDER, exist_ok=True)
os.makedirs(NOTES_FOLDER, exist_ok=True)

# Get the current date and time for the log file name
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = os.path.join(LOGS_FOLDER, f"note_app_log_{current_datetime}.log")

# Configure the logger
try:
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
except FileNotFoundError:
    # If there's an issue with the log file path, print an error message
    print(f"Error: Unable to create log file at '{LOG_FILE}'. Please check the path.")
    raise  # Raise the exception to terminate the program

def register_user(username, password):
    try:
        user_folder = os.path.join(NOTES_FOLDER, username)

        # Check if the username is already taken
        if os.path.exists(user_folder):
            print("\nUsername already taken. Please choose another username.")
            return

        # Create a folder for the user within the "notes" directory
        os.makedirs(user_folder)

        # Store user information in the "users.txt" file
        with open(USERS_FILE, 'a') as file:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            file.write(f"{username}:{hashed_password}\n")
            print("\nUser registered successfully.")

        logging.info(f"User '{username}' registered successfully.")
    except Exception as e:
        logging.error(f"Error during user registration: {str(e)}")

def login():
    try:
        while True:
            username = input("\nEnter your username: ")
            password = input("\nEnter your password: ")

            # Check if the user is the admin
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                logging.info(f"Admin '{ADMIN_USERNAME}' logged in successfully.")
                return ADMIN_USERNAME
               
            # Check if the user exists in the "users.txt" file
            with open(USERS_FILE, 'r') as file:
                for line in file:
                    stored_username, stored_hashed_password = line.strip().split(':')
                    if stored_username == username and hashlib.sha256(password.encode()).hexdigest() == stored_hashed_password:
                        user_folder = os.path.join(NOTES_FOLDER, username)
                        logging.info(f"User '{username}' logged in successfully.")
                        return username

                # Inform the user if the login was unsuccessful
                print("\nInvalid username or password. Please try again.")
                return None
    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        return None

def admin_read_notes():
    try:
        notes_exist = False  # Flag to check if any notes exist

        print("\nReading Notes for All Users:")

        for user_folder in os.listdir(NOTES_FOLDER):
            user_path = os.path.join(NOTES_FOLDER, user_folder)

            if os.path.isdir(user_path):
                for note in os.listdir(user_path):
                    note_path = os.path.join(user_path, note)

                    with open(note_path, 'r') as file:
                        note_content = file.read()

                    print(f"\n----- {note} -----\n")
                    print(note_content)
                    print("\n----- End of Note -----")

                    notes_exist = True  # Set the flag since at least one note is found

        if not notes_exist:
            print("\nNo notes found for any user.")

        logging.info(f"Admin '{ADMIN_USERNAME}' read notes for all users.")
    except Exception as e:
        logging.error(f"Error reading notes for all users: {str(e)}")

def admin_delete_notes():
    try:
        notes_exist = False  # Flag to check if any notes exist

        print("\nDeleting Notes for All Users:")

        for user_folder in os.listdir(NOTES_FOLDER):
            user_path = os.path.join(NOTES_FOLDER, user_folder)
            
            if os.path.isdir(user_path):
                for note in os.listdir(user_path):
                    note_path = os.path.join(user_path, note)
                    os.remove(note_path)
                    logging.info(f"Note '{note}' deleted by Admin '{ADMIN_USERNAME}'.")
                    print(f"\nNote '{note}' deleted successfully.")
                    
                    notes_exist = True  # Set the flag since at least one note is deleted

        if notes_exist:
            print("\nAll notes deleted.")
        elif not notes_exist:
            print("\nNo notes found for any user. Nothing to delete.")
    except Exception as e:
        logging.error(f"Error deleting notes for all users: {str(e)}")

def create_note(username):
    try:
        while True:
            title = input("\nEnter the title of the note: ")
            content = input("\nEnter the content of the note: ")

            user_folder = os.path.join(NOTES_FOLDER, username)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(user_folder, f"{title}.txt")

            with open(filename, 'w') as file:
                file.write(f"Author: {username}\n")
                file.write(f"Date: {timestamp}\n\n")
                file.write(content)

            logging.info(f"Note created by '{username}': {title}")

            another_note = input("\nDo you want to create another note? (yes/no): ")
            if another_note.lower() != 'yes':
                break
    except Exception as e:
        logging.error(f"Error during note creation: {str(e)}")

def list_notes(username):
    try:
        user_folder = os.path.join(NOTES_FOLDER, username)
        notes = [f for f in os.listdir(user_folder) if f.endswith(".txt")]

        if notes:
            print("\nList of Notes:\n")
            for note in notes:
                print(note)
        else:
            print("\nNo notes found.")
    except Exception as e:
        logging.error(f"Error listing notes: {str(e)}")
        
def delete_note(username):
    try:
        user_folder = os.path.join(NOTES_FOLDER, username)
        notes = [f for f in os.listdir(user_folder) if f.endswith(".txt")]

        if notes:
            print("\nList of Notes:\n")
            for i, note in enumerate(notes, 1):
                print(f"{i}. {note}")

            note_index = int(input("\nEnter the index of the note you want to delete: ")) - 1

            if 0 <= note_index < len(notes):
                note_to_delete = notes[note_index]
                note_path = os.path.join(user_folder, note_to_delete)
                
                # Confirm deletion
                confirm_delete = input(f"\nAre you sure you want to delete '{note_to_delete}'? (yes/no): ")
                if confirm_delete.lower() == 'yes':
                    os.remove(note_path)
                    logging.info(f"Note '{note_to_delete}' deleted by '{username}'.")
                    print(f"\nNote '{note_to_delete}' deleted successfully.")
                else:
                    print("\nDeletion canceled.")
            else:
                print("\nInvalid note index. Please try again.")
        else:
            print("\nNo notes found.")
    except Exception as e:
        logging.error(f"Error deleting note: {str(e)}")
        
def read_note(username):
    try:
        user_folder = os.path.join(NOTES_FOLDER, username)
        notes = [f for f in os.listdir(user_folder) if f.endswith(".txt")]

        if notes:
            print("\nList of Notes:\n")
            for i, note in enumerate(notes, 1):
                print(f"{i}. {note}")

            note_index = int(input("\nEnter the index of the note you want to read: ")) - 1

            if 0 <= note_index < len(notes):
                note_to_read = notes[note_index]
                note_path = os.path.join(user_folder, note_to_read)

                with open(note_path, 'r') as file:
                    note_content = file.read()

                print(f"\n----- {note_to_read} -----\n")
                print(note_content)
                print("\n----- End of Note -----\n")

                logging.info(f"Note '{note_to_read}' read by '{username}'.")
            else:
                print("\nInvalid note index. Please try again.")
        else:
            print("\nNo notes found.")
    except Exception as e:
        logging.error(f"Error reading note: {str(e)}")

try:
    while True:
        action = input("\nChoose an action: \n1. Login\n2. Register\n3. Admin \n4. Quit\n> ")

        if action == '1':
            logged_in_user = login()
            if logged_in_user:
                while True:
                    note_action = input("\nChoose an action: \n1. Create a note\n2. List all notes\n3. Read a note\n4. Delete a note\n5. Logout\n> ")
                    if note_action == '1':
                        create_note(logged_in_user)
                    elif note_action == '2':
                        list_notes(logged_in_user)
                    elif note_action == '3':
                        read_note(logged_in_user)
                    elif note_action == '4':
                        delete_note(logged_in_user)
                    elif note_action == '5':
                        logging.info(f"User '{logged_in_user}' logged out.")
                        break

                    else:
                        print("\nInvalid action. Please try again.")

        elif action == '2':
            new_username = input("\nEnter your desired username: ")
            new_password = input("\nEnter your password: ")
            register_user(new_username, new_password)
            logging.info(f"User '{new_username}' registered successfully.")
        
        elif action == '3':
            admin_password = input("\nEnter admin password: ")
            if admin_password == ADMIN_PASSWORD:
                admin_action = input("\nChoose an Admin Action:\n1. Read Notes (for all users)\n2. Delete Notes (for all users)\n> ")
                if admin_action == '1':
                    admin_read_notes()
                elif admin_action == '2':
                    admin_delete_notes()
                else:
                    print("\nInvalid admin action.")
            else:
                print("\nInvalid admin password.")
        
        elif action == '4':
            logging.info("Program exited.")
            break

        else:
            print("\nInvalid action. Please try again.")
except Exception as e:
    logging.error(f"Error in the main program: {str(e)}")
