import os

from flask import Flask
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv

bootstrap = Bootstrap()
load_dotenv()


def create_app(test_config=None):
    # create and configure the nutrition
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )
    bootstrap.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Load blueprints
    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint="index")

    from . import auth
    app.register_blueprint(auth.bp)

    from . import calorie
    app.register_blueprint(calorie.bp)

    return app
