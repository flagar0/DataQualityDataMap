import debugpy
from os import name


def init():
    if name == "nt":
        if not debugpy.is_client_connected():
            debugpy.listen(("localhost", 5678))
            debugpy.wait_for_client()  # Only include this line if you always want to attach the debugger
