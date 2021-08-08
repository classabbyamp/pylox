import argparse

from .lox import Lox


parser = argparse.ArgumentParser(prog="pylox",
                                 description="A Lox interpreter. Run with no arguments to use the REPL.")
parser.add_argument("-d", "--dot", type=str, required=False, action="store", dest="dot",
                    help="output a graphviz representation of the AST to the specified file. Does not work for REPL")
group = parser.add_mutually_exclusive_group()
group.add_argument("-c", type=str, metavar="CMD", dest="cmd", action="store",
                   help="run an inline Lox script")
group.add_argument("script", type=str, metavar="SCRIPT", nargs="?",
                   help="the filename of the Lox script to run")

args = parser.parse_args()

try:
    if args.script:
        Lox.run_file(path=args.script, dot=args.dot)
    elif args.cmd:
        Lox.run_inline(cmd=args.cmd, dot=args.dot)
    else:
        Lox.run_prompt()
except KeyboardInterrupt:
    raise SystemExit(130)
