from flask import render_template as HTML, make_response as Response
from flask_jwt_extended.utils import create_refresh_token, create_access_token
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.admin import AdminModel
from helpers.utils import hash
from messages import response_errors as Err
from messages import responses_success as Succ


class AdminLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be blank"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank"
    )

    @classmethod
    def post(cls):
        # Get data from parser
        data = cls.parser.parse_args()

        # Find admin from db
        admin = AdminModel.find_by_username(data["username"])

        # Check password
        if admin and admin.password == hash(data["password"]):
            # Create access token
            access_token = create_access_token(identity=admin.id, fresh=True)

            # Create refresh token
            refresh_token = create_refresh_token(admin.id)

            return Succ.SUCCESS_AUTHENTICATED(access_token, refresh_token)

        return Err.ERROR_INVALID_CREDS


class AdminManage(Resource):
    # [GET] Manage admin page
    @jwt_required
    def get(self):
        headers = {"Content-Type": "text/html"}
        return Response(HTML("admin_management.html"), 200, headers)
