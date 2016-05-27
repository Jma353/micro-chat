# Methods to compose HTTP response JSON 
from flask import jsonify


def http_json(result, bool):
	result.update({ "success": bool })
	print result
	return jsonify(result)


def http_resource(result, name, bool=True):
	resp = { "data": { name : result }}
	return http_json(resp, bool)


def http_errors(result): 
	errors = { "data" : { "errors" : result.errors["_schema"] }}
	return http_json(errors, False)


