from starlette.templating import Jinja2Templates
import os


templates = Jinja2Templates(os.environ["TEMPLATES_DIR"])

def datetime_format(value, format="%B %m, %Y"):
    return value.strftime(format)

templates.env.filters["datetime_format"] = datetime_format
