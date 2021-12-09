from flask import Flask
import logging

log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__, static_url_path='/',
            static_folder='build/html')

@app.route('/')
@app.route('/<path:path>')
def serve_sphinx_docs(path='index.html'):
    return app.send_static_file(path)

app.run(debug=False)
