#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import sys
from flask import Flask
from flask import jsonify
from flask_swagger import swagger
from api.utils.database import db
from api.utils.responses import response_with
import api.utils.responses as resp
from api.routes.routes_general import route_path_general


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    app.register_blueprint(route_path_general, url_prefix='/api')

    # START GLOBAL HTTP CONFIGURATIONS
    @app.after_request
    def add_header(response):
        return response

    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)

    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp.NOT_FOUND_HANDLER_404)

    # END GLOBAL HTTP CONFIGURATIONS

    db.init_app(app)
    with app.app_context():
        db.create_all()

    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
                        level=logging.DEBUG)
    return app