import yaml
import logging.config
from importlib import resources
from pathlib import Path
from config import resources as config_resources

LOG_CONFIG_FILE = "config_logger.yaml"
LOGS_FOLDER = "./logs/"

def loadLoggerConfig(nombreFicheroYaml=str(resources.files(config_resources).joinpath(LOG_CONFIG_FILE))):
   with open(nombreFicheroYaml, 'r') as stream:
      config = dict(yaml.load(stream, Loader=yaml.FullLoader))
      if config.get("handlers", {"file":None}).get("file", {"filename":None}).get("filename"):
         config["handlers"]["file"]["filename"] = LOGS_FOLDER + "app.log"
      logging.config.dictConfig(config)
      
if __name__ == "__main__":
    print(Path.cwd())
    loadLoggerConfig()
    
    import logging
    logger = logging.getLogger("test_config")
    logger.info("Prueba de logger. Mensaje de info")
    logger.debug("Mensaje desde debug")