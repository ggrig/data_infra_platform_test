import os
import configparser

import logging
logger = logging.getLogger(__name__)


class Config:

    # class variable __instance will keep track of the singleton object instance
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Config,cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if(self.__initialized): return

        self.settings = configparser.ConfigParser()
        current_directory = os.path.dirname(os.path.realpath(__file__))
        self.settings.read(os.path.join(current_directory,'config.ini'))
        
        self.__initialized = True
    
    def _get(self, section:str, option:str):
        retval = None
        try:
            retval = self.settings.get(section, option)
        except Exception as ex:
            logger.error(str(ex))
        return retval

    def _getboolean(self, section:str, option:str):
        retval = None
        try:
            retval = self.settings.getboolean(section, option)
        except Exception as ex:
            logger.error(str(ex))
        return retval

    @property
    def production(self)->bool:
        return self._production()

    def _log_level(self)->str:
        return self._get('General', 'log_level')

    @property
    def log_level(self)->str:
        return self._log_level()

    def _aws_account(self)->str:
        return self._get('General', 'aws_account')
 
    @property
    def aws_account(self)->str:
        return self._aws_account()

    def _region(self)->str:
        return self._get('Regions', 'region')

    @property
    def region(self)->str:
        return self._region()

    def _vpc_name(self)->str:
        return (self._get('VPC','vpc_name'))

    @property
    def vpc_name(self)->str:
        return self._vpc_name()

    def _cdk_logic_stack_name(self)->str:
        return ("TestECSStak")

    @property
    def cdk_logic_stack_name(self)->str:
        return self._cdk_logic_stack_name()




