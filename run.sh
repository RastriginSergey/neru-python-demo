#!/bin/bash

nodemon --exec python3 -m debugpy --listen localhost:9229 main.py
# nodemon --exec python3 main.py

# --wait-for-client

# entrypoint:
#     - python3
#     - main.py