from utils import search, lend_book, on_exit, display_result
from time import time
def prompter(books, users, **kwargs):
    
    try:
        options = [
            "Search the book database for a book by Author surname",
            "Search the user database for a user by surname",
            "Lend a book to a user",
            "Exit from the system"
        ]

        length = max(list(map(lambda option: len(option), options)))

        while True:
            print('')
            print("Enter Ctrl+C to exit")
            prompt = '> '
            print("".rjust(length + 10, '-'))
            for index, option in enumerate(options):
                print(f'{index+1}) {option}'.rjust(16))

            print("".rjust(64, '-'))
            print(prompt, end='')
            selected = input("Select an option from the list above using the number: ")
            if(selected.isdigit() and int(selected) > 0 and int(selected) < 5):
                if(selected == "1"):
                    while True:
                        author_name = input("$ Enter the Author's surname: ")
                        if not author_name.isdigit():
                            result = search(author_name, books)
                            display_result(result)
                            break

                if(selected == "2"):
                    while True:
                        user_name = input(f"$$ Enter the User's surname: ")
                        if not user_name.isdigit():
                            result = search(user_name, users)
                            display_result(result)
                            break

                if(selected == "3"):
                    books, users = lend_book(books, users)
                    
                if(selected == "4"):
                    on_exit(books, users, kwargs["b"], kwargs["u"])

    except KeyboardInterrupt:
        print("\nExiting...")
        
        