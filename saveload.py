from constants import ALL_RECORDS
import pickle


def writing_data_to_file():
    if ALL_RECORDS:
        with open('databook.pickle', 'wb') as f:
            pickle.dump(ALL_RECORDS, f)
    else:
        with open('databook.pickle', 'wb') as f:
            pickle.dump(None, f)


def reading_data_from_file():
    try:
        with open('databook.pickle', 'rb') as f:
            NEW_RECORDS = pickle.load(f)
            return NEW_RECORDS
    except EOFError:
        pass
