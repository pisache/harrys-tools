import sys

from scanPDF import scan

def main():
    print("MAIN")

    dir = sys.argv[1]
    scan(dir)

if __name__ == "__main__":
    main()