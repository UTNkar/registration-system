import os
import sys
sys.path.append(os.path.abspath(os.path.join('..', 'registrationSystem', 'registrationSystem')))
from settings.base import DATABASES
import getopt
import names
import psycopg2

def usage():
    print((
        "Usage:\n"
        "\t-h, --help\tDisplay this usage message\n"
        "\t-n, --non=\tSet number of non-UTN members to generate (default 0)\n"
        "\t-u, --utn=\tSet number of UTN members to generate (default 0)\n"
        "\t-s, --status=\tSet status of generated interest checks (default \"waiting\")"
    ))

def create_users(status, is_utn_member, number):
     return  ["{}".format(create_user(status, is_utn_member)) for x in range(number)]

def create_user(status, is_utn_member):
    name = names.get_full_name()
    email = name.split()[1].lower() + "@gmail.com"
    return (name, email, 19980704-0000, status, is_utn_member)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:s:u:", ["help", "non=", "status=", "utn="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    non_members = 0
    utn_members = 0
    status = "waiting"
    for k, v in opts:
        if k in ("-h", "--help"):
            usage()
            sys.exit()
        elif k in ("-n", "--non"):
            non_members = v
        elif u in ("-u", "--utn"):
            utn_members = v
        elif k in ("-s", "--status"):
            if v in ("waiting", "mail unconfirmed", "won", "lost", "accepted", "declined"):
                status = v
            else:
                assert False, "Error: invalid interest check status"
        
        else:
            assert False, "Error: unhandled option"

    confirm = input((
        "This will create:\n"
        "\t{} non-UTN member interest checks\n"
        "\t{} UTN member interest checks\n"
        "With status \"{}\"\n"
        "Is this ok? [y/n]\n")
        .format(non_members, utn_members, status)
    )
    
    if(confirm.lower() == "y"):
        # This will take the DB credentials from the django settings files
        connection = psycopg2.connect(
            user = DATABASES["default"]["USER"],
            password = DATABASES["default"]["PASSWORD"],
            host = DATABASES["default"]["HOST"],
            port = DATABASES["default"]["PORT"],
            database = DATABASES["default"]["NAME"]
        )

        cursor = connection.cursor()

        insert_query = 'insert into \"registrationSystem_interestcheck\" (name, email, person_nr, status, is_utn_member) values '
            
        if non_members != 0:
            non_members_data = ", ".join(create_users(status, False, int(non_members)))
            cursor.execute(insert_query + non_members_data)
            print(non_members_data)
            print("Inserted non-UTN members")

        if utn_members != 0:
            utn_members_data = ", ".join(create_users(status, True, int(utn_members)))
            cursor.execute(insert_query + utn_members_data)
            print("Inserted UTN members")

        connection.commit()
        print("Successefully created new interestchecks")
        cursor.close()
        connection.close()
            
if __name__ == "__main__":
    main()
