# Standard
from __future__ import annotations
from typing import TYPE_CHECKING
import sys
import threading as th

# External
import nikocraft as nc

# Local
from constants import *
if TYPE_CHECKING:
    from main import Main


class UserManager(th.Thread):

    def __init__(self, main: Main):

        super(UserManager, self).__init__(name="User Manager")


