from flask import Flask, jsonify, request, Blueprint
from app.db import get_transac_por_concepto

transacs = Blueprint("transacs_api_v1", 
                     "transacs_api_v1", 
                     url_prefix="/api/v1/transacs")

@transacs.route("/hello", methods=["GET"])
def apiHello():
    return jsonify({"message":"Hello, my boy!"})

@transacs.route('/greet/<name>', methods=['GET'])
def greet(name):
    return jsonify({"message": f"Hello, {name}! Welcome to the API."})

@transacs.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    a = data.get("a", 0)
    b = data.get("b", 0)
    return jsonify({"result":a+b})

@transacs.route("/<concepto>", methods=["GET"])
def getTransacs(concepto):
    return jsonify(get_transac_por_concepto(concepto=concepto))