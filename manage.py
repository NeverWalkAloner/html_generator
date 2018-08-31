# python imports
import argparse

# project imports
from core.managers import execute


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sitename", type=str, dest="sitename", default='My site'
    )
    parser.add_argument("--paginatedby", type=int, dest="paginatedby")
    args = parser.parse_args()
    execute(args)
