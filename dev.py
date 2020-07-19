import argparse
from connector import app
from connector.env import DEBUG, APP_PORT


def main():
    parser = argparse.ArgumentParser(description='External Connection API used in the SNAP system')
    parser.add_argument('--run',
                        action='store_true',
                        help="Runs App"
                        )

    args = parser.parse_args()

    if args.run:
        # Enter Execution Code here
        app.run(debug=DEBUG, port=APP_PORT, host="0.0.0.0")


if __name__ == "__main__":
    main()
