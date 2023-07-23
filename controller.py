# Standard
import sys
import argparse as ap
from multiprocessing.connection import Client
from multiprocessing import AuthenticationError


# Main
if __name__ == '__main__':

    parser = ap.ArgumentParser(
        prog="python controller.py",
        description="A CLI tool to send some tasks to the arcade software.",
        allow_abbrev=False
    )

    parser.add_argument("-v", "--verbose", help="log detailed information", action="store_true")
    parser.add_argument("-p", "--port", help="which port to use", type=int, default=42000)
    parser.add_argument("key", help="the authentication key")
    parser.add_argument("task", help="the task to execute")
    parser.add_argument("args", help="arguments for the task", nargs="*")

    args = parser.parse_args()

    key = "DefaultKey" if args.key == "-" else args.key

    if args.verbose:
        print(f"Try to open connection with port {args.port} ...")
    try:
        conn = Client(("localhost", args.port), authkey=key.encode("utf-8"))
        if args.verbose:
            print(f"Connection successful opened!")
    except ConnectionError:
        print(f"Connection failed! Cannot find listener on port {args.port}!")
        sys.exit(1)
    except AuthenticationError:
        print(f"Connection failed! Invalid key '{args.key}'!")
        sys.exit(1)

    if args.verbose:
        print(f"Send task '{args.task}' with arguments {args.args} ...")
    conn.send({"type": args.task, "args": args.args})

    code, message = conn.recv()

    if code == 0:
        if message:
            print("Task executed successfully! Message:")
            print(f"    {message}")
        else:
            print("Task executed successfully!")
    else:
        print(f"Task execution failed! Error {code}:")
        print(f"    {message}")

    if args.verbose:
        print("Close connection ...")
    conn.close()
