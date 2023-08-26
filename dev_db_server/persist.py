import pickle, os, threading

from .users import Users, Json

save_file = os.path.join(os.path.dirname(__file__), "SAVE_DB.PK")


def load():
    try:
        data_file = open(save_file, "rb")
        Users.users_by_identifier = pickle.load(data_file) or Json()
        data_file.close()

        Users.users_by_api_key = {
            user.api_key: user for user in Users.users_by_identifier.values()
        }

        threading.Thread(target=Users.watch).start()
        print("Loading Finished")

    except (FileNotFoundError, EOFError) as e:
        print(f"Loading Error: {e}")


def save():
    try:
        data_file = open(save_file, "wb")
        pickle.dump(Users.users_by_identifier, data_file)
        data_file.close()

        print("Saving Finished")
    except Exception as e:
        print(f"Saving Error: {e}")


def load_t():
    threading.Thread(target=load).start()


def save_t():
    threading.Thread(target=save).start()
