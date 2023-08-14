from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {
            'status': 'success' if 'error' not in data else 'error',
            'data': data,
            'statusCode': renderer_context['response'].status_code
        }

        return super().render(response_data, accepted_media_type, renderer_context)
