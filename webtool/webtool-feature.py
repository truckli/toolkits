#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import os

from tornado.options import define, options

define("port", default=8018, help="run on the given port", type=int)


class FadHandler(tornado.web.RequestHandler):
    def reader_markdown(self, report_fname):
        if not os.path.isfile(report_fname):
            self.write('Server Error. Computation result not generated')
            return

        render_fname = report_fname + '.html'
        #convert .md file into .html file
        os.system('markdown %s > %s' % (report_fname, render_fname))
        if not os.path.isfile(render_fname):
            self.write('Server Error. Render file not generated')
            return

        report_f = open(render_fname)
        self.write(report_f.read())
        report_f.close()

    def start_html(self, title=None):
        self.write('<html><body>')
        if type(title) == type('string'):
            self.write('<title>%s </title><h2>%s</h2>' % (title, title))
        else:
            pass

    def end_html(self):
        self.write('</body></html>')


    def get(self):
        self.start_html('Feature Calculation')
        self.write(
                'Usage: input a dataset and a feature name, and this tool will do some statistics<br><br>'
                '<form action="/" method="post">'
                '<label>Data File Name: </label>'
                '<input type="text" name="dataset" value="reorder_label_train_merge_5feature.final.fad"><br>'
                '<label>Feature Name: </label>'
                '<input type="text" name="feature" value="mAfHotWordNumInTitle"><br>'
                '<label>Use no caching </label>'
                '<input type="checkbox" id="recalc" name="recalc"><br>'
                '<input type="submit" value="Submit"><br>'
                '</form>'
                )
        self.reader_markdown('README.md')
        self.end_html()

    def post(self):
        feature_name = self.get_argument("feature")
        data_fname = self.get_argument("dataset")
        cb_list = self.get_arguments("recalc")
        recalc = False
        if len(cb_list) > 0:
            recalc = True
        
        report_fname = data_fname + '--' + feature_name + '.md' 
        if recalc or not os.path.isfile(report_fname):
            os.system('./feature.py %s %s > %s' % (data_fname, feature_name, report_fname))
        
        self.start_html(title = feature_name.encode('utf-8'))
        self.reader_markdown(report_fname)
        self.end_html()
        
        
def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", FadHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()




