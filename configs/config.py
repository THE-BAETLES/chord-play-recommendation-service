from dotenv import dotenv_values
from injector import Binder, Injector, SingletonScope, singleton
class Configuration:
    def __init__(self, config):
        self.config = config

def get_development_config(binder: Binder):
    configuration = Configuration({**dotenv_values("development.env")})    
    binder.bind(Configuration, to=configuration, scope=singleton)

