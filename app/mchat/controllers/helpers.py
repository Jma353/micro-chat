# Methods to compose HTTP response JSON 
from flask import jsonify

def http_json(result, bool):
	result.update({ "success": bool })
	return jsonify(result)


def http_resource(result, name):
	resp = { "data": { name : result.data }}
	return http_json(resp, True)

def http_errors(result): 
	errors = { "data" : { "errors" : result.errors["_schema"] }}
	return http_json(errors, False)
