from starlette.templating import Jinja2Templates
import os


templates = Jinja2Templates(os.environ["TEMPLATES_DIR"])
