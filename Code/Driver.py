import options


def main():

    choice = 1

    while choice != 4:

        print("\n------- RobMe Bank -------")
        print("1. Sign Up (New Customer) ")
        print("2. Sign In (Existing Customer) ")
        print("3. Admin Sign In ")
        print("4. Quit ")

        try:
            choice = int(input())

        except:
            print("Invalid Choice")
            choice = 1
            continue

        if choice == 1:
            options.signUp()

        elif choice == 2:
            options.signIn()

        elif choice == 3:
            options.adminSignIn()

        elif choice == 4:
            print("Thanks!! \nHappy banking!\n")

        else:
            print("Invalid Choice")


main()
