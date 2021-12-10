import sys


def run(example_name):
    if example_name == 'pdf_reader':
        from examples import pdf_reader
        pdf_reader.main()

    else:
        sys.exit('Example not found, available examples: pdf_reader')


if __name__ == '__main__':
    print("Running example: {}".format(sys.argv[1]))
    len(sys.argv) < 2 and sys.exit('Usage: %s <example_name>' % sys.argv[0])

    run(sys.argv[1])

    sys.exit(0)
