import argparse
from typing import List

from composer.definition import DefinitionComposer
from definers.free_dictionary_api import FreeDictionaryDefiner
from definers.json_storage import JsonDefinerStorage
from definers.multi_source import MultiSourceDefinerWithStorage
from middlewares.cefr import CEFRLimiter
from middlewares.char import CharLengthValidator
from middlewares.meaningful_words import MeaningfulWords
from middlewares.numbers import Number
from models.definer import Definer
from models.middleware import Middleware
from models.reader import Reader
from models.tokenizer import Tokenizer
from models.writer import Writer
from readers.pdfminer_reader import PDFMinerReader
from readers.pypdf_reader import PyPDFReader
from readers.text import TextReader
from readers.url_reader import URLReader
from tokenizers.mwe_tokenize import MWETokenizer
from writers.csv_writer import CSVWriter
from writers.json_writer import JsonFileWriter


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Do you want an explain for hard word in a text or audio file?')
    parser.add_argument('-i', '--input', help='the file to explain', type=str)
    parser.add_argument(
        '-t', '--input-type', help='the file type, Default = text', type=str,
        choices=['text', 'url', 'pdf'], default='text'
    )
    parser.add_argument(
        '--pdf-engine', help='the pdf engine, Default = pdfminer', type=str,
        choices=['pdfminer', 'pyPdf'], default='pdfminer'
    )
    parser.add_argument('-o', '--output', help='the output file', type=str)
    parser.add_argument(
        '-ot', '--output-type', help='the output file type, Default = json', type=str,
        choices=['json', 'csv'], default='json'
    )
    parser.add_argument('--csv-write-header', help='write header in csv output', action='store_true')
    parser.add_argument(
        '--cefr-level', help='minimum word\'s cefr level to consider, default = B1', type=str,
        choices=['A1', 'A2', 'B1', 'B2', 'C1', 'C2'], default='B1'
    )
    parser.add_argument(
        '--ignore-unknown-cefr', help='ignore words with unknown cefr level, default = False',
        default=False, action='store_true'
    )
    parser.add_argument(
        '-v', '--verbose', help='verbose mode', default=False, action='store_true'
    )

    parser.add_argument(
        '--disable-meaningful-words-filter',
        help='by default we try to filter out meaningless words, this option disable it',
        action='store_true'
    )

    parser.add_argument(
        '--char-limiter-min-length',
        help='minimum length of the word to consider, default = 3',
        type=int, default=3
    )

    parser.add_argument(
        '--disable-char-limiter-filter',
        help='by default we try to filter out words with too few characters, this option disable it',
        action='store_true'
    )
    args = parser.parse_args()
    return args


def get_reader(args: argparse.Namespace) -> Reader:
    print("reading from {}".format(args.input))
    if args.input_type == 'text':
        print('Using TextReader')
        return TextReader(args.input)
    elif args.input_type == 'url':
        print('Using URLReader')
        return URLReader(args.input)
    elif args.input_type == 'pdf' and args.pdf_engine == 'pdfminer':
        print('Using PDFMinerReader')
        return PDFMinerReader(file_path=args.input)
    elif args.input_type == 'pdf' and args.pdf_engine == 'pyPdf':
        print('Using PyPDFReader')
        return PyPDFReader(file_path=args.input)

    raise Exception('Unknown input type')


def get_writer(args: argparse.Namespace) -> Writer:
    print("writing to {}".format(args.output))
    if args.output_type == 'json':
        print('output file type is json')
        return JsonFileWriter(args.output)
    if args.output_type == 'csv':
        print('output file type is csv')
        return CSVWriter(args.output)

    raise Exception('Unknown output type')


def get_tokenizer(_: argparse.Namespace) -> Tokenizer:
    return MWETokenizer()


def get_middlewares(args: argparse.Namespace) -> List[Middleware]:
    rules = [
        (Number(), True),
        (CharLengthValidator(min_length=args.char_limiter_min_length), not args.disable_char_limiter_filter),
        (MeaningfulWords(), not args.disable_meaningful_words_filter),
        (CEFRLimiter(min_cefr=args.cefr_level, filter_unknowns=not args.ignore_unknown_cefr),
         not args.disable_meaningful_words_filter)
    ]

    return list(rule[0] for rule in rules if rule[1])


def get_definer(_: argparse.Namespace) -> Definer:
    return MultiSourceDefinerWithStorage(
        storage=JsonDefinerStorage(),
        definers=[
            FreeDictionaryDefiner(),
        ]
    )


def get_definition_composer(args: argparse.Namespace) -> DefinitionComposer:
    return DefinitionComposer(
        tokenizer=get_tokenizer(args),
        middlewares=get_middlewares(args),
        definer=get_definer(args),
        verbose=args.verbose
    )


def main():
    args = get_arguments()
    reader = get_reader(args)
    writer = get_writer(args)

    composer = get_definition_composer(args)
    composer.compose_write(reader=reader, writer=writer)


if __name__ == '__main__':
    main()
