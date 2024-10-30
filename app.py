from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import jwt
from pydantic import BaseModel, EmailStr, ValidationError, Field




app = Flask(__name__)
CORS(app)


class UserModel(BaseModel):
    email: EmailStr | None = Field(..., description="Email is required")
    name: str | None = Field(..., description="Name is required")
    age: int = Field(..., description="Age is required")

    @classmethod
    def validate_age(cls, age:int) -> bool:
        return age >= 18 and age <= 40
    
@app.route("/query", methods=["GET"])
def root():
    if request.method != "GET":
        abort(405)
    
    try:
        req = {
            "email": request.args.get("email"),
            "name": request.args.get("name"),
            "age": int(request.args.get("age"))
        }
        data = UserModel(**req)

        if UserModel.validate_age(req["age"]) != True:
            abort(400, description="Age must be between 18 and 40")
        
        return jsonify({
            "payload": data.model_dump()
        }), 200
    
    except ValidationError as e:
        abort(400, description=e.errors())
    
    except ValueError as e:
        abort(400, description=str(e))


@app.errorhandler(400)
@app.errorhandler(405)
@app.errorhandler(500)
def error_handler(error):
    return jsonify({
        "status_code": error.code,
        "message": error.description
    })


if __name__ == '__main__':
    app.run(debug=True)