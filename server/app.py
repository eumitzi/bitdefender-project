from flask import Flask
from views.scanHash import scan_hash
from views.scanBuffer import scan_buffer
from views.uploadFile import upload_file
from views.downloadFile import download_file

app = Flask(__name__)
app.register_blueprint(scan_hash)
app.register_blueprint(scan_buffer)
app.register_blueprint(upload_file)
app.register_blueprint(download_file)
