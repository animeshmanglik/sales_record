#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import make_response, jsonify

BAD_REQUEST_400 = {
    "http_code": 400,
    "code": "badRequest",
    "message": "Bad request"
}

SERVER_ERROR_500 = {
    "http_code": 500,
    "code": "serverError",
    "message": "Server error"
}

NOT_FOUND_HANDLER_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "There are no such handler"
}

SUCCESS_200 = {
    'http_code': 200,
    'code': 'success'
}


def response_with(response, value=None, message=None, error=None, headers={}):
    result = {}
    if value is not None:
        result.update(value)

    if response.get('message', None) is not None:
        result.update({'message': response['message']})

    result.update({'code': response['code']})

    if error is not None:
        result.update({'errors': error})

    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'Sales Record API'})

    return make_response(jsonify(result), response['http_code'], headers)
