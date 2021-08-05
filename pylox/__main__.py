import sys

from .lox import Lox


if __name__ == "__main__":
    try:
        if len(sys.argv) > 2:
            print("Usage: python -m pylox [script]")
            raise SystemExit(64)
        elif len(sys.argv) == 2:
            Lox.run_file(sys.argv[1])
        else:
            Lox.run_prompt()
    except KeyboardInterrupt:
        raise SystemExit(130)
