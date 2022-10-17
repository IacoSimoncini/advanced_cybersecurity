from download import download
from unzip import unzip
from clean import clean
import configparser

def menu():
    print("-----------------------------MENU-------------------------------")
    print("choose the task to be performed by pressing the associated key: ")
    print("d) download file GARR")
    print("u) unzip and create dataset GARR")
    print("c) clean dataset GARR")
    print("e) exit")
    print("\nSpecial thanks for the layout to Aldo Drago Franconi")
    print("----------------------------------------------------------------")
    print("\nYour choice: ")

def main():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        menu()
        key=input()
        while(key!="e"):
            if key=="d":
                download(config)
            elif key=="u":
                unzip(config)
            elif key=="c":               
                #clean(config)
                pass
            else:
                print("wrong key...retry")
            menu()
            key=input()
    except FileNotFoundError:
        print("can't find config.ini, you can find how to create it in readMe")

if __name__ == "__main__":
    main()