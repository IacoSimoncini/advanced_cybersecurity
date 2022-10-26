from download import download
from unzip import unzip
from remove import remove
from transform import transform
import configparser

def menu():
    print("-----------------------------MENU-------------------------------")
    print("choose the task to be performed by pressing the associated key: ")
    print("d) download file GARR")
    print("u) unzip and create dataset GARR")
    #print("c) remove duplicates dataset GARR")
    print("t) transform dataset in uni-bi-trigrams")
    print("e) exit")
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
            elif key=="r":               
                #remove(config)
                pass
            elif key=="t":
                transform(config)
            else:
                print("wrong key...retry")
            menu()
            key=input()
    except FileNotFoundError:
        print("can't find config.ini, you can find how to create it in readMe")

if __name__ == "__main__":
    main()