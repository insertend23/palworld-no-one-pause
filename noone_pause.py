import time
from src.palserver_controller import PalServerController
from src.config_loader import ConfigLoader


def main():
    config = ConfigLoader().load()
    if not config:
        print("Cannot load config file")
        return
    controller = PalServerController(config)

    while True:
        if not controller.is_server_running():
            print("Server is not running.")
            controller.start_server()
        else:
            print("Players in server:")
            print(*controller.get_players(), sep="\n")

            # Loop until there are no players
            if controller.has_players():
                print("Players found. Server will continue running.")
                time.sleep(60)
                continue
            # Restart server to prevent memory leaks
            else:
                print("No players in server. Restart the server.")
                controller.restart_server()

        # If there's no players, pause server
        if controller.is_server_running() and not controller.has_players():
            print("Restart complete. Pause the server.")
            controller.pause_server()
        else:
            continue

        # Wait until packet is captured
        print("Waiting for the server packet to be captured.")
        controller.capture_server_packet()

        # Resume server if players try to connect
        print("Connection attempt has been detected")
        print("Resume server")
        controller.resume_server()


if __name__ == "__main__":
    main()
