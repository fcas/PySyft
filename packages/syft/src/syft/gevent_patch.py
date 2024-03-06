# stdlib
import os


def str_to_bool(bool_str: str | None) -> bool:
    result = False
    bool_str = str(bool_str).lower()
    if bool_str == "true" or bool_str == "1":
        result = True
    return result


GEVENT_MONKEYPATCH = str_to_bool(os.environ.get("GEVENT_MONKEYPATCH", "False"))

# 🟡 TODO 30: Move this to where we manage the different concurrency modes later
# make sure its stable in containers and other run targets
# if GEVENT_MONKEYPATCH:
#     monkey.patch_all(ssl=False)


def is_notebook() -> bool:
    # third party
    from IPython import get_ipython

    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


jupyter_notebook = is_notebook()
