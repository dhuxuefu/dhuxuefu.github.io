# -*- coding: utf-8 -*-
"""Local dev server with no-cache headers (avoids stale fetch during testing)."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os, sys

os.chdir(r"C:\Users\86152\Desktop\net\dhu-xuefu")

class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stdout.write("[dev] %s\n" % (fmt % args))

ThreadingHTTPServer(("127.0.0.1", 8001), NoCacheHandler).serve_forever()
