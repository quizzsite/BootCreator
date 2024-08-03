from app import db
from app import runServ as create_app

import logging
logging.basicConfig(level=logging.INFO)
create_app()