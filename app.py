#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect
from util import decorators
from flask import render_template

app = Flask(__name__)
app.debug = True
allowed_methods = ['POST', 'GET']


@app.route('/echo', methods=allowed_methods)
def echo():
    return 'echo'


@app.route('/home', methods=allowed_methods)
def home():
    if request.method == 'POST':
        return redirect('/home', code=302)
    return render_template(['templates', 'home.tmpl'], **data)


@app.route('/logs', methods=allowed_methods)
def logs():
    import os
    def tail(f, n):
        grep = request.args.get('grep', '')
        stdin, stdout = os.popen2('tail -n {0} {1} | grep "{2}"'.format(n, f, grep))
        stdin.close()
        lines = stdout.readlines()
        stdout.close()
        lines.reverse()
        return lines
    file_path = os.path.join(settings.base_dir, settings.log_dir, 'debug.log')
    res = tail(file_path, 30)
    return '<br />'.join(res)



if __name__ == '__main__':
    run_simple('localhost', 5000, app, use_debugger=True)