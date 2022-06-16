""" Provides dynamic message with spinner or progressbar """
from time import sleep
from threading import Thread
from telegram import Message
import telegram


class SPINNERS:
    """ Provides different spinner collections """

    EYES = ["◡◡", "⊙⊙", "◠◠"]
    SQUARES = "▖▘▝▗"


class ProgressMsg:
    """ Provides dynamic message with spinner or progressbar """

    def __init__(self, reply_to: Message, text='', spinning=True, spinner=SPINNERS.SQUARES):
        self.__reply_to = reply_to
        self.__text = text
        self.__spinning = spinning
        self.__progress = 0
        self.__spinner = spinner
        self.__active = True
        self.__delay = 0.2
        self.__init_msg()
        self.__thread = Thread(target=self.__perform_loop)
        self.__thread.start()

    def __init_msg(self):
        """ Send initial dynamic message and save it's identifier """
        if self.__spinning:
            self.__msg = self.__reply_to.reply_text(
                '   '.join([self.__text, self.__spinner[self.__progress]]))

    def __update_msg(self):
        """ Update current dynamic message with new spinner/progress value """
        if self.__spinning:
            self.__msg.edit_text('   '.join([self.__text, self.__spinner[self.__progress]]))

    def __stop(self):
        """ Stop message update sycle """
        self.__active = False

    def finish(self):
        """ Stop message updates and update it to finish state """
        self.__stop()
        try:
            self.__msg.edit_text('   '.join([self.__text, '✓']))
        except telegram.error.BadRequest:
            pass

    def __perform_loop(self):
        """ Perform dynamic message update loop

        * Should be executed in separate thread *

        """
        while self.__active:
            if self.__spinning:
                self.__progress = (self.__progress + 1) % len(self.__spinner)
            self.__update_msg()
            sleep(self.__delay)
