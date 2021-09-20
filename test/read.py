# arguements for main

from argparse import ArgumentParser
from main import *
parser = ArgumentParser()

parser.add_argument("--write_tree", type=int, default=1, help='0: no; 1: yes')
parser.add_argument("--write_result", type=int, default=1, help='0: no; 1: yes')
parser.add_argument("--select_span", type=int, default=0, help='0: no; 1: yes')
# readfile format
# sentence number
# sentence
# verb
# relation/ comment
parser.add_argument("--read", type=str, default="inputs./data_frame", help='name of file to read from')
args = parser.parse_args()
runall(args)