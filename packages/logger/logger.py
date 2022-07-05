import logging
import configparser
import os


class LoggerException(Exception):
    pass


class Logger(logging.getLoggerClass()):

    DEFAULT_CONFIG_FNAME = "config.ini"

    CONFIG_FIELD_LEVEL = "level"
    CONFIG_FIELD_FILE_NAME = "log_file_name"

    # acceptable format for its value like:
    # {name} | {levelname} | {asctime} | {message}
    CONFIG_FIELD_FORMAT = "format"

    def __init__(self, name="", config=None, source_dir=None, *args, **kwargs):
        """Initialization."""
        super().__init__(name, *args, **kwargs)
        try:
            self.__init_configs(config)
            # Get config values
            configData = self.__get_valid_config(
                Logger.CONFIG_FIELD_LEVEL,
                Logger.CONFIG_FIELD_FORMAT,
                Logger.CONFIG_FIELD_FILE_NAME,
            )
            self.setLevel(configData[Logger.CONFIG_FIELD_LEVEL])
            self.__addHandlers(configData, source_dir)
        except LoggerException as er:
            raise Exception("Error of logger initialization:" + er)

    # def error(self, msg, *arg1, **arg2):
    #     print('ERROR: ' + msg)
    #     super().error(msg, *arg1, **arg2)

    def __addHandlers(self, configData, source_dir):
        """Add file & console (for debug) handlers."""
        hdlr = self.__get_file_hadler(configData, source_dir)
        self.addHandler(hdlr)

        # add console output for DEBUG level
        if self.level == logging.DEBUG:
            # fmt: off
            format = self.__decode_format(
                configData[Logger.CONFIG_FIELD_FORMAT]
            )
            # fmt: on
            ch = logging.StreamHandler()
            ch.setFormatter(logging.Formatter(format))
            self.addHandler(ch)

    def __init_configs(self, cnfg=None):
        """Init 2 configration objects: external and internal.
        when ext. obj does not have a value it will be taken from int. one.
        """
        self.__config = cnfg
        self.__def_config = self.__get_config_by_default()
        if self.__config is None:
            # Use the local {Logger.DEFAULT_CONFIG_FNAME} by default
            self.__config = self.__def_config

        if self.__config is None:
            raise LoggerException("config is not initialized properly")

    def __decode_format(self, fstr) -> str:
        """Decode format from '{}' to '%()s'."""
        if fstr is None:
            return ""
        return fstr.replace("{", "%(").replace("}", ")s")

    def __get_valid_config(self, *conf_field_names) -> dict:
        """Get config values by their names."""
        res = {}
        for name in conf_field_names:
            res[name] = self.__get_valid_config_field_value(name)
        return res

    def __get_valid_config_field_value(self, conf_field_name):
        """Get config field value and validate it."""
        val = (
            # fmt: off
            self.__config[conf_field_name] \
            if conf_field_name in self.__config \
            else None
            # fmt: on
        )
        if val is None:
            # Default value
            val = (
                # fmt: off
                self.__def_config[conf_field_name] \
                if conf_field_name in self.__def_config \
                else None
                # fmt: on
            )
        if val is None:
            raise LoggerException(
                "Config field:", conf_field_name, " Value is not found"
            )
        return val

    def __get_config_by_default(self):
        """Config by default. Used for getting default values."""
        root_dir = os.path.dirname(os.path.abspath(__file__))
        fname = os.path.join(root_dir, Logger.DEFAULT_CONFIG_FNAME)
        config = configparser.ConfigParser()
        config.read(fname)
        return config["DEFAULT"]

    def __get_file_hadler(self, confValues, output_dir):
        """Get file handler for logging."""

        # Get full file name for logging
        if output_dir is None:
            # Set the current dir by default
            output_dir = os.path.dirname(os.path.abspath(__file__))
        # fmt: off
        full_fname = os.path.join(
            output_dir,
            confValues[Logger.CONFIG_FIELD_FILE_NAME]
        )
        # fmt: on
        format = self.__decode_format(confValues[Logger.CONFIG_FIELD_FORMAT])

        handler = logging.FileHandler(full_fname, mode="a")
        handler.setLevel(confValues[Logger.CONFIG_FIELD_LEVEL])
        handler.setFormatter(logging.Formatter(format))
        return handler

    @staticmethod
    def test():
        print("test started")

        log = Logger(name="test")
        log.debug("test debug")
        log.info("test info")
        log.warning("test warn")
        log.error("test error")
        log.critical("test critical")

        print("test done")


# Do NOT run as the main
if __name__ == "__main__":
    raise Exception("do NOT run it as the main module")
    # Logger.test()
