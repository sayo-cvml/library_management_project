from prompter import prompter
from utils import load_data, parse_args


args = parse_args()
    
if __name__ == "__main__":

    books_data, users_data = load_data(args)
    books_keys = books_data.keys
    books = books_data.get("data")
    users_keys = users_data.keys
    users = users_data.get("data")
    prompter(books, users, b=args.b, u=args.u)

    