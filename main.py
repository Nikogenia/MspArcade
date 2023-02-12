# Standard
import sys
import threading as th

# External
import nikocraft as nc

# Local
from constants import *
from configs import MainConfig, GameConfig
from window import Window


class Main(nc.App):

    def __init__(self, args):

        super(Main, self).__init__(args,
                                   name="Maker Space Arcade",
                                   author="MakerSpace",
                                   version="Alpha 1.1.1",
                                   short_description="A Maker Space project for an arcade machine in the school",
                                   description="This is the main software of the arcade machine, which controls " +
                                   "all games and provides a menu. The gaming machine is a project of the Maker " +
                                   "Space for the Bodensee Gymnasium Lindau in Germany.",
                                   details="Developers:\n- Nikocraft (aka Nikolas)\n- MakerSam (aka Samuel)\n- Valentin\n- Linus",
                                   log_path=PATH_LOG)

        # Create directories
        for path in [PATH_CONFIG, PATH_GAME]:
            if not nc.file.exists(path):
                nc.file.make_dir(path, self.logger)

        # Load configs
        self.logger.info("Load configs ...")
        self.main_config: MainConfig = MainConfig(self.logger)
        self.game_config: GameConfig = GameConfig(self.logger)
        self.main_config.load()
        self.game_config.load()

        # TODO Initialize game manager

        # Initialize window
        self.window = Window(self)

    def run(self):

        # TODO Initialize game manager

        # Open window
        self.window.open()

    def quit(self):

        # Save configs
        self.logger.info("Save configs ...")
        self.main_config.save()
        self.game_config.save()


# Main
if __name__ == '__main__':

    # Initialize main
    main = Main(sys.argv)

    # Start main
    main.start()
