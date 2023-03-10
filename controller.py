# Standard
import sys
import argparse as ap
from multiprocessing.connection import Client
from multiprocessing import AuthenticationError


# Main
if __name__ == '__main__':

    parser = ap.ArgumentParser(
        prog="Controller",
        description="A CLI tool to send some tasks to the arcade software.",
        allow_abbrev=False
    )

    parser.add_argument("key", help="The authentication key")
    parser.add_argument("task", help="The task to execute")
    parser.add_argument("-p", "--port", help="Which port to use", type=int, default=42000)

    args = parser.parse_args()

    print("Try to open connection ...")
    try:
        conn = Client(("localhost", args.port), authkey=args.key.encode("utf-8"))
        print("Connection successful!")
    except ConnectionError:
        print(f"Connection failed! Cannot find listener on port {args.port}!")
        sys.exit(1)
    except AuthenticationError:
        print("Connection failed! Invalid key!")
        sys.exit(1)

    print("Send task ...")
    conn.send({"type": args.task})

    print("Close connection ...")
    conn.close()
