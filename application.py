import argparse
import os
from server import application, sio

# run the application.
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', action='store_true')
    args = parser.parse_args()
    if args.l:
        sio.run(application, debug=True, host='0.0.0.0', port=8000)
    else:
        sio.run(application)