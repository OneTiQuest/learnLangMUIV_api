from flask import Blueprint, jsonify, request, send_file
import base64, uuid
from flask_jwt_extended import jwt_required

files_bp = Blueprint("files", __name__, url_prefix="/files")


@files_bp.post("/")
@jwt_required()
def load():
    file = request.json.get("file")
    if "base64," in file:
        meta, base64_string = file.split("base64,")

        file_family, file_type = meta.split("data:")[1].split(";")[0].split("/")

        decoded_file = base64.b64decode(base64_string)

        file_id = uuid.uuid4()
        file_name = f"{file_id}.{file_type}"
        file_path = f"./files/{file_name}"

        with open(file_path, "wb") as new_file:
            new_file.write(decoded_file)

        return jsonify(file_name)


@files_bp.get("/<string:file_name>")
@jwt_required()
def get_file(file_name: str):
    file_path = f"../files/{file_name}"
    return send_file(file_path)
