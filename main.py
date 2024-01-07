# Standard
import sys
import threading as th
import traceback as tb
import shutil

# External
import nikocraft as nc

# Local
from constants import *
from configs import MainConfig, GameConfig, UserConfig
from window.window import Window
from user.user_manager import UserManager
from game.game_manager import GameManager
from listener import Listener
import email_utils


class Main(nc.App):

    def __init__(self, args):

        super(Main, self).__init__(args,
                                   name="Msp Arcade",
                                   author="Makerspace",
                                   version="1.0.0",
                                   short_description="A Makerspace project for an arcade machine in the school",
                                   description="This is the main software of the arcade machine, which controls " +
                                   "all games and provides a menu. The gaming machine is a project of the " +
                                   "Makerspace for the Bodensee Gymnasium Lindau in Germany.",
                                   details="Database: Lernplattform Mebis Bayern (Moodle)\n\n" +
                                   "TEAM\n" +
                                   "Management: Dr. Andre Scherl\n"
                                   "Software: Nikogenia (aka Nikolas)\n" +
                                   "Hardware:\n" +
                                   "- Valis World (aka Valentin)\n" +
                                   "- Linicus (aka Linus)\n" +
                                   "- ...\n" +
                                   "Games: checkout menu",
                                   log_path=PATH_LOG,
                                   log_thread=True)

        self.running = True

        # Create directories
        for path in [PATH_CONFIG, PATH_CONFIG_BACKUP, PATH_GAME]:
            if not nc.file.exists(path):
                nc.file.make_dir(path, self.logger)

        # Load configs
        self.main_config: MainConfig = MainConfig(self.logger)
        self.game_config: GameConfig = GameConfig(self.logger)
        self.user_config: UserConfig = UserConfig(self.logger)
        self.logger.info("Backup configs ...")
        for conf in (self.main_config, self.game_config, self.user_config):
            try:
                self.logger.debug(f"Copy config '{conf.path}' to '{PATH_CONFIG_BACKUP}' ...")
                shutil.copy(conf.path, PATH_CONFIG_BACKUP)
            except OSError:
                pass
        self.logger.info("Load configs ...")
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

        # Initialize listener
        self.listener: Listener = Listener(self)

    def run(self):

        # Start user manager
        self.user_manager.start()

        # Start game manager
        self.game_manager.start()

        # Start listener
        self.listener.start()

        try:

            # Open window
            self.window.open()

        except Exception:
            self.handle_crash()
            self.logger.info("Close window ...")
            self.window.scene.quit()
            self.window.scene.deactivate_event_hooks()
            self.window.quit()
        except KeyboardInterrupt:
            self.logger.warning("Keyboard interrupted! Shutting down!")
            self.logger.info("Close window ...")
            self.running = False
            self.window.running = False
            self.window.scene.quit()
            self.window.scene.deactivate_event_hooks()
            self.window.quit()

    def quit(self):

        # Quit game manager
        self.game_manager.running = False
        self.game_manager.join()

        # Quit user manager
        self.user_manager.running = False
        self.user_manager.join()

        # Quit listener
        self.listener.running = False
        self.listener.join()

        # Save configs
        self.logger.info("Save configs ...")
        self.user_config.save()

    def handle_crash(self):

        # Set exit code
        self.exit_code = 1

        # Log error
        self.logger.critical("\n" +
                             "----------------------------------------\n" +
                             "       CRITICAL UNEXPECTED ERROR\n" +
                             (
                                "                Restart\n"
                                if self.main_config.restart_on_crash else
                                "                 Exit\n"
                             ) +
                             "----------------------------------------\n" +
                             tb.format_exc() +
                             "----------------------------------------")

        # Quit all components
        self.running = False
        self.window.running = False
        self.game_manager.running = False
        self.user_manager.running = False
        self.listener.running = False

        # Send email, if activated
        if self.main_config.email_send:
            email_utils.send_error(self.main_config, tb.format_exc().strip("\n"))


def main():

    # Set main thread name
    th.main_thread().name = "Main"

    # Initialize main
    m = Main(sys.argv)

    # Start main
    exit_code = m.start()

    # Check for restart
    if exit_code == 2 or (exit_code == 1 and m.main_config.restart_on_crash and nc.time.run_time() > 8):
        print("")
        print("RESTART")
        print("")
        nc.time.wait(3)
        main()


# Main
if __name__ == '__main__':
    main()
