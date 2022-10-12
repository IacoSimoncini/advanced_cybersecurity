from download import download
from unzip import unzip
from clean import clean
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

def main():
    while(True):
        print("-----------------------------MENU-------------------------------")
        print("choose the task to be performed by pressing the associated key :")
        print("d) download file GARR")
        print("u) unzip and create dataset GARR")
        print("c) clean dataset GARR")
        print("e) exit")
        print("\nSpecial thanks for the layout to Aldo Drago Franconi")
        print("----------------------------------------------------------------")
        print("\nYour choice: ")
        key=input()
        if key=="d":
            download(config)
        elif key=="u":
            unzip(config)
        elif key=="c":
            pass
        elif key=="e":
            break
        else:
            print("wrong key...retry")

if __name__ == "__main__":
    main()