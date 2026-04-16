from client import Client
from server import Server

def main():
    while True:
        choice = input("[c]lient or [s]erver? ").strip()

        if choice == "c":
            c = Client(1111)
            c.getSecureCode()
            c.mainloop()

            break
        elif choice == "s":
            s = Server(1111)

            s.mainloop()

            break

        print("Invalid choice")

if __name__ == "__main__":
    main()