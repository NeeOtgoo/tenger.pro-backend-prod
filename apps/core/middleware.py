

class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):

        response = 123

        return response