import argparse
import functools
from pprint import pprint

def load_data(args):

    def to_dict(item, keys):
        _dict = {}
        data = item.strip().split(",")
        for index, field in enumerate(data):
            _dict[keys[index]] = field
        return _dict


    with open(f'{args.b}') as library:
        books = library.readlines()
        books_keys = books[0].strip().split(",")

    with open(f'{args.u}') as users_db:
        users = users_db.readlines()
        users_keys = users[0].strip().split(",")

    books_data = {
        'keys': books_keys,
        'data': list(map(functools.partial(to_dict, keys=books_keys), books[1:]))
        }

    users_data = {
        'keys': users_keys, 
        'data': list(map(functools.partial(to_dict, keys=users_keys), users[1:]))
        }
        
    return books_data, users_data

def search(param, db):
    bank = db.copy()
    if param == "*":
        return bank
    if param.isdigit():
        search_field = 'user_library_number' if 'user_library_number' in bank[-1].keys() else 'book_id'
    else:
        search_field = 'user_surname' if 'user_surname' in bank[-1].keys() else 'author_surname'
    results = filter(lambda item: item[search_field] == param, bank)
    return list(results)



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', type=str, required=True, help="books csv file path")
    parser.add_argument('-u', type=str, required=True, help="users csv file path")
    args, _ = parser.parse_known_args()
    return args


def lend_book(books, users):
    loan_limit = 4
    book_exists = False
    user_exists = False
    while True:
        user_id = input(f"$$$ Enter the User ID: ")

        if user_id.isdigit(): 
            user = search(user_id, users)
            if len(user) > 0:
                user_exists = True
                print("Accepted: User exists.")
                display_result(user)
                break
            else:
                print("Rejected: User does not exist.")

        else:
            print("Enter a valid ID")

    while True:
        book_id = input(f"$$$ Enter the Book ID: ")
        if book_id.isdigit(): 
            book = search(book_id, books)
            if len(book) > 0:
                book_exists = True
                print("Accepted: Book exists")
                display_result(book)
                break
            else:
                print("Rejected: Book does not exist")

    if book_exists and user_exists:
        if book[0]['on_loan_to'].isdigit():
            print("Book is on loan")
        else:
            books_on_loan = []
            for key, value in user[0].items():
                if "books_on_loan" in key and value.isdigit():
                    books_on_loan.append(value)
            
            count = len(books_on_loan)
            if count >= loan_limit:
                print(f'Maximum number of books borrowed by {user[0]["user_firstname"]} {user[0]["user_surname"]}')
            else:
                update_user = user[0]
                update_book = book[0]
                books = list(filter(lambda book: book["book_id"] != update_book["book_id"], books))
                users = list(filter(lambda user: user["user_library_number"] != update_user["user_library_number"], users))
                update_book["on_loan_to"] = update_user["user_library_number"]
                update_user[f"books_on_loan{count+1}"] = update_book["book_id"]
                books.append(update_book)
                users.append(update_user)
                books.sort(key=lambda book: int(book["book_id"]))
                users.sort(key=lambda user: int(user["user_library_number"]))
                print(f'The book {update_book["title"]} has been successfully loaned to {update_user["user_firstname"]} {update_user["user_surname"]}.')

        return books, users



def on_exit(books, users, books_file, users_file):

    def write_file(contents, file):
        with open(file, 'w') as fp:
            fp.write(f'{",".join(contents[0].keys())}\n')
            lines = list(map(lambda content: f'{",".join(content.values())}\n', contents))
            for line in lines:
                fp.write(line)

    print("Saving...")
    write_file(books, 'new_'+books_file)
    write_file(users, 'new_'+users_file)
    print("Saved")
    exit(0)


def display_result(results):
    if results:
        if "book_id" in results[0].keys():

            headings = ["Book ID", "Author", "Title", "on loan"]
            format_str = "{:<10} {:<30} {:<50} {:<23}"
            print(format_str.format(*headings))
            for result in results:
                print(format_str.format(
                    result["book_id"],
                    f"{result['author_firstname']} {result['author_surname']}",
                    result["title"],
                    "Yes" if result["on_loan_to"] else "No"
                    )
                )
            return

        if "user_library_number" in results[0].keys():
            headings = ["User ID", "User", "Borrowed Book 1", "Borrowed Book 2", "Borrowed Book 3", "Borrowed Book 4"]
            format_str = "{:<10} {:<30} {:<30} {:<30} {:<30} {:<30}"
            print(format_str.format(*headings))
            for result in results:
                print(format_str.format(
                    result["user_library_number"],
                    f"{result['user_firstname']} {result['user_surname']}",
                    result["books_on_loan1"],
                    result["books_on_loan2"],
                    result["books_on_loan3"],
                    result["books_on_loan4"],
                    )
                )
            return

    else:
        print("No results")
    
    
