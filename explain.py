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
    parser = argparse.ArgumentParser(description='Do you want an explain for hard in a text or audio file?')
    parser.add_argument('-i', '--input', help='the file to explain', type=str)
    parser.add_argument(
        '-t', '--input-type', help='the file type', type=str, choices=['text', 'url', 'pdf'], defualt='text'
    )
    parser.add_argument(
        '--pdf-engine', help='the pdf engine', type=str, choices=['pdfminer', 'pyPdf'], default='pdfminer'
    )
    parser.add_argument('-o', '--output', help='the output file', type=str)
    parser.add_argument('-ot', '--output-type', help='the output file type', type=str, choices=['json', 'csv'])
    parser.add_argument(
        '--cefr-level', help='the cefr level', type=str, choices=['A1', 'A2', 'B1', 'B2', 'C1', 'C2'], default='B1'
    )
    parser.add_argument('--ignore-unknown-cefr', help='ignore words with unknown cefr level', type=bool, default=False)
    args = parser.parse_args()
    return args


def get_reader(args: argparse.Namespace) -> Reader:
    if args.input_type == 'text':
        return TextReader(args.input)
    elif args.input_type == 'url':
        return URLReader(args.input)
    elif args.input_type == 'pdf' and args.pdf_engines == 'pdfminer':
        return PDFMinerReader(file_path=args.input)
    elif args.input_type == 'pdf' and args.pdf_engines == 'pyPdf':
        return PyPDFReader(file_path=args.input)

    raise Exception('Unknown input type')


def get_writer(args: argparse.Namespace) -> Writer:
    if args.output_type == 'json':
        return JsonFileWriter(args.output)
    if args.output_type == 'csv':
        return CSVWriter(args.output)

    raise Exception('Unknown output type')


def get_tokenizer(_: argparse.Namespace) -> Tokenizer:
    return MWETokenizer()


def get_middlewares(args: argparse.Namespace) -> List[Middleware]:
    return [
        Number(),
        CharLengthValidator(min_length=3),
        MeaningfulWords(),
        CEFRLimiter(min_cefr=args.cefr_level, filter_unknowns=args.ignore_unknown_cefr)
    ]


def get_definer(_: argparse.Namespace) -> Definer:
    return MultiSourceDefinerWithStorage(
        storage=JsonDefinerStorage(),
        definers=[
            FreeDictionaryDefiner(),
        ]
    )


def main():
    args = get_arguments()
    reader = get_reader(args)
    writer = get_writer(args)
    tokenizer = get_tokenizer(args)
    middlewares = get_middlewares(args)
    definer = get_definer(args)
    composer = DefinitionComposer(tokenizer=tokenizer, middlewares=middlewares, definer=definer)

    composer.compose_write(reader=reader, writer=writer)

