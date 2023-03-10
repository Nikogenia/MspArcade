# FILE PATHS

# Resource directories
PATH_RESOURCE = "./resources"
PATH_IMAGE = f"{PATH_RESOURCE}/images"
PATH_FONT = f"{PATH_RESOURCE}/fonts"

# Data directories
PATH_DATA = "./data"
PATH_LOG = f"{PATH_DATA}/logs"
PATH_CONFIG = f"{PATH_DATA}/configs"
PATH_GAME = f"{PATH_DATA}/games"


# GUI

# Window
GUI_WIDTH = 1920
GUI_HEIGHT = 1080
GUI_FPS = 30

# Log FPS and output on quit
FPS_LOG = False

# Show debug screen by default
SHOW_FPS_DEFAULT = False

# Disable scaling on windows
DISABLE_RESOLUTION_SCALING = False


# USER

# Database
DATABASE_URL = "https://lernplattform.mebis.bayern.de/webservice/rest/server.php"

# Time management of new accounts
DEFAULT_TIME = 300
TIME_RESET_TIMEOUT = 1000

# Database update timeout
AUTO_UPDATE = 300
FAST_UPDATE = 22

# Display accounts on debug screen
# WARNING: Disable in production! Security risk!
SHOW_USERS_IN_DEBUG_SCREEN = True


# ERROR HANDLING

# Restart on crash
RESTART_ON_CRASH = False
