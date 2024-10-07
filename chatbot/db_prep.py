from dotenv import load_dotenv
from db import init_db

load_dotenv()

def main():
    print(f'Initializing database...')
    init_db()


if __name__ == "__main__":
    main()