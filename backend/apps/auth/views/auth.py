from flask import g, request
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from apps.auth.views.authschema import UserSchema
from apps.utils.jwt_util import generate_tokens
from apps.utils.middlewares import verify_jwt
from apps.utils.responser import Responser
from apps.utils.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

# class Auth(Resource):
#     """
#     认证
#     """
#     method_decorators = {
#         'put': [login_required]
#     }

schema = UserSchema()


class Login(Resource):
    """
       登录
   """
    parser = reqparse.RequestParser()
    parser.add_argument('Login', type=str, required=True, help="Every store needs a name.")

    def post(self):

        data = self.parser.parse_args()
        try:
            # 使用 Marshmallow 的 Schema 来验证数据
            user = schema.load(data)
            token, refresh_token, expire_time = generate_tokens(user['username'])
            result = {'accessToken': token, 'refreshToken': refresh_token, "username": user['username'],
                      "expires": expire_time, "roles": ["admin"]}
            return Responser.response_success(code=HTTP_201_CREATED, data=result)

        except ValidationError as err:
            return Responser.response_error(msg=err.messages, code=HTTP_400_BAD_REQUEST)


class Sign(Resource):
    """
    注册
    """
    parser = reqparse.RequestParser()
    parser.add_argument('Sign', type=str, required=True, help="Every store needs a name.")

    def post(self):
        data = self.parser.parse_args()
        try:
            schema.create_user(data)
            return Responser.response_success(code=HTTP_200_OK, msg='注册成功！')
        except ValidationError as err:
            return Responser.response_error(msg=err.messages, code=HTTP_400_BAD_REQUEST)


class RefreshToken(Resource):
    """
       刷新token
   """
    """
    1.携带刷新token,返回业务token
    2.用户必须登录g.username , 必须携带刷新token不允许携带业务token
    3.客户端请求参数 刷新token
    """

    # method_decorators = {
    #     'post': [login_required]
    # }

    def post(self):
        token = request.json.get('refreshToken')
        if token:
            payload = verify_jwt(token)
            "判断token的校验结果"
            if payload:
                "获取载荷中的信息赋值给g对象"
                g.username = payload.get('username')
                g.refresh = payload.get('refresh')

            # '1.判断是否登录 2.判断refresh字段是否为True--是否是刷新token'
            if g.username and g.refresh is True:
                # '调用生成token的方法 参数 need_refresh_token=False 不需要生成刷新token 仅生成业务token'
                token, refresh_token, expire_time = generate_tokens(g.username, need_refresh_token=False)
                # '返回业务token  修改成功状态码201'
                result = {'accessToken': token, 'refreshToken': token, "expires": expire_time}
                return Responser.response_success(code=HTTP_201_CREATED, data=result)

        # '失败返回错误信息和状态码'
        return Responser.response_error(code=HTTP_400_BAD_REQUEST)


class AsyncRoute(Resource):
    """
    动态生成路由,大型项目使用
    """

    def get(self):
        data = [{
            "path": "/permission",
            "meta": {
                "title": "权限管理",
                "icon": "lollipop",
                "rank": 10
            },
            "children": [
                {
                    "path": "/permission/page/index",
                    "name": "PermissionPage",
                    "meta": {
                        "title": "页面权限",
                        "roles": ["admin", "common"]
                    }
                },
                {
                    "path": "/permission/button/index",
                    "name": "PermissionButton",
                    "meta": {
                        "title": "按钮权限",
                        "roles": ["admin", "common"],
                        "auths": ["btn_add", "btn_edit", "btn_delete"]
                    }
                }
            ]
        }]
        return Responser.response_success(data=data)
