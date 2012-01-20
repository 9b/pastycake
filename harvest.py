import sys

from gather import main


if __name__ == "__main__":
    sys.argv = sys.argv[0:1] + ['harvest', ] + sys.argv[1:0]
    main()
