import json
class HttpResponseMixin(object):
    def render_to_http_response(self):
        pass

    def json_response_data(self,data):
        p_dict = json.loads(data)
        final_data = []
        for i in p_dict:
            final_data.append(i['fields'])
        j_d = json.dumps(final_data)
        return j_d