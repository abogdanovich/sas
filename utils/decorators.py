#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import functools


def jsonify(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, dict):
            # result = json.dumps(result, cls=JSONEncoder)
            result = json.dumps(result)
            # self.req.setHeader('Content-Type', 'application/json; charset=UTF-8')
        # result = encode.utf8(result)
        return result
    return wrapper


def json_response(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        assert isinstance(result, dict), 'Data error. Dictionary is required.'
        result.update({'rc': 0})
        # return dict(rc=0, data=result)
        return result
    return wrapper


def form_params(req_type, **params):
    assert req_type in ('POST', 'GET'), 'Only POST or GET allowed'

    def decorator(method):
        @functools.wraps(method)
        def wrapper(self):
            # We support only form-params
            prepared = {}
            for key, parser in params.items():
                v = self.post_param(key) if req_type == 'POST' else self.get_param(key)
                value = parser(v) if v is not None else v
                prepared[key] = value
            return method(self, **prepared)
        return wrapper
    return decorator


form_post = functools.partial(form_params, 'POST')
form_get = functools.partial(form_params, 'GET')