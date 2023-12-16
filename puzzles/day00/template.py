import argparse


def puzzle(filename):
    return (1, 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    result = puzzle(args.filename)
    print(f"{result[0]}, {result[1]}")


if __name__ == "__main__":
    main()
