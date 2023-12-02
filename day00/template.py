import argparse


def puzzle(filename):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    puzzle(args.filename)
