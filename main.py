# Standard
import sys
import threading as th

# External
import nikocraft as nc

# Local
from constants import *
from configs import MainConfig, GameConfig, UserConfig
from window.window import Window
from user.user_manager import UserManager
from game.game_manager import GameManager


class Main(nc.App):

    def __init__(self, args):

        super(Main, self).__init__(args,
                                   name="Arcade",
                                   author="MakerSpace",
                                   version="Alpha 1.1.1",
                                   short_description="A Maker Space project for an arcade machine in the school",
                                   description="This is the main software of the arcade machine, which controls " +
                                   "all games and provides a menu. The gaming machine is a project of the Maker " +
                                   "Space for the Bodensee Gymnasium Lindau in Germany.",
                                   details="Developers:\n- Nikocraft (aka Nikolas)\n- MakerSam (aka Samuel)\n- Valentin\n- Linus",
                                   log_path=PATH_LOG,
                                   log_thread=True)

        self.running = True

        # Create directories
        for path in [PATH_CONFIG, PATH_GAME]:
            if not nc.file.exists(path):
                nc.file.make_dir(path, self.logger)

        # Load configs
        self.logger.info("Load configs ...")
        self.main_config: MainConfig = MainConfig(self.logger)
        self.game_config: GameConfig = GameConfig(self.logger)
        self.user_config: UserConfig = UserConfig(self.logger)
        self.main_config.load()
        self.game_config.load()
        self.user_config.load()
        self.main_config.save()
        self.game_config.save()
        self.user_config.save()

        # Initialize window
        self.window = Window(self)

        # Initialize user manager
        self.user_manager: UserManager = UserManager(self)

        # Initialize game manager
        self.game_manager: GameManager = GameManager(self)

    def run(self):

        # Start user manager
        self.user_manager.start()

        # Start game manager
        self.game_manager.start()

        try:

            # Open window
            self.window.open()

        except Exception:
            self.running = False
            self.game_manager.running = False
            self.user_manager.running = False
            raise

    def quit(self):

        # Quit game manager
        self.game_manager.running = False
        self.game_manager.join()

        # Quit user manager
        self.user_manager.running = False
        self.user_manager.join()

        # Save configs
        self.logger.info("Save configs ...")
        self.user_config.save()


# Main
if __name__ == '__main__':

    # Set main thread name
    th.main_thread().name = "Main"

    # Initialize main
    main = Main(sys.argv)

    # Start main
    main.start()
