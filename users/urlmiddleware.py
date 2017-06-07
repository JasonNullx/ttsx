# coding:utf-8


class UrlMiddleware(object):
    def process_response(self, request, response):
        url_list = [
            '/users/register/',
            '/users/register_handle/',
            '/users/register_exist/',
            '/users/login/',
            '/users/login',
            '/users/login_handle/',
            '/users/login_handle',
            '/users/logout/',
            '/js/jquery-1.12.2.js/',
            '/cart/count_change/',
        ]
        if not request.is_ajax() and request.path not in url_list:
            response.set_cookie('red_url', request.get_full_path())
        return response
