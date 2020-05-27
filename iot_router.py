import sys
import os
import io

from twisted.logger import globalLogPublisher, jsonFileLogObserver, FileLogObserver, eventAsText

from Router.Config import Config
from Router.TwistedWebServer.Server import Server







def main():

    if Config.get('logging')['verbose'] is True:
        globalLogPublisher.addObserver(FileLogObserver(sys.stdout, lambda e: eventAsText(e) + "\n"))

    if Config.get('logging')['log_to_file'] is True:
        logfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), "logs/log.json")
        globalLogPublisher.addObserver(jsonFileLogObserver(io.open(logfile, 'w+'), ''))

    server = Server(Config.get('server')['port'])
    server.run()









if __name__ == "__main__":
    main()
