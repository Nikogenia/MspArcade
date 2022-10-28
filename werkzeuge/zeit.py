# System Module
import time as _tm
import datetime as _dt


# Warte
def warte(dauer: float):
    _tm.sleep(dauer)


# Protokollierung
def protokollierung():
    return _dt.datetime.now().strftime("%Y-%m-%d_%Hh-%Mm-%Ss")


# Laufzeit Zeit
def laufzeit_zeit():
    return _tm.perf_counter()
