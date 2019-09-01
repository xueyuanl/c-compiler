from lexer import lexer


def main():
    file_name = 'source.c'
    source_file = open(file_name, 'r')
    str = source_file.read()

    lexer(str)


if __name__ == '__main__':
    main()
