from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg import openapi
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class RegisterSchema(SwaggerAutoSchema):
    def get_response_schemas(self, response_serializers):
        response_schemas = super().get_response_schemas(response_serializers)
        response_schemas['201'] = openapi.Response(
            description=None,
            examples={
                'application/json': {
                    'status': 'OK',
                }
            }
        )

        return response_schemas


class VerifyUserSchema(SwaggerAutoSchema):
    def get_response_serializers(self):
        response_serializers = super().get_response_serializers()
        response_serializers['201'] = TokenRefreshSerializer

        return response_serializers
