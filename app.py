import uuid
import base64
import binascii
from datetime import datetime
import time
import hashlib
import hmac

from flask import Flask, render_template, request

from improc.improc import convertImageToJSON
app = Flask(__name__)

diagram = "none"

class Token:
    def __init__(self, key, appID, userName, vCardFile, expires):
        self.type = 'provision'
        self.key = key
        self.jid = userName + "@" + appID
        if (vCardFile):
            self.vCard = read_file(vCardFile).decode("utf-8").strip()
        else:
            self.vCard = ""
        self.expires = expires

    def __str__(self):
        return "Token" + {'type': self.type,
                          'key': self.key,
                          'jid': self.jid,
                          'vCard': self.vCard[:10] + "...",
                          'expires': self.expires}.__str__()

    def serialize(self):
        sep = b"\0"  # Separator is a NULL character
        body = to_bytes(self.type) + sep + to_bytes(self.jid) + sep + to_bytes(self.expires) + sep + to_bytes(
            self.vCard)
        mac = hmac.new(bytearray(self.key, 'utf8'), msg=body, digestmod=hashlib.sha384).digest()
        serialized = body + sep + binascii.hexlify(mac)
        return serialized


def to_bytes(o):
    return str(o).encode("utf-8")


def generate_token(user_name):
    epoch = 62167219200
    key = 'dc8b8d68d296424eb57f21b20cf76947'
    app_id = '2503e0.vidyo.io'
    expires_in_secs = 60 * 5

    d = datetime.now()
    expires = epoch + int(time.mktime(d.timetuple())) + int(expires_in_secs)

    token = Token(key, app_id, user_name, None, expires)
    serialized = token.serialize()
    b64 = base64.b64encode(serialized)
    return b64.decode()


@app.route('/')
def homepage():
    my_token = generate_token(uuid.uuid4().hex)
    return render_template('app.html', token=my_token)


@app.route('/diagram', methods=['POST'])
def make_diagram():
    raw = request.form['data']
    prefix = "data:image/png;base64,"
    b64s = raw[len(prefix):]

    file_path = '/tmp/' + uuid.uuid4().hex + ".png";
    file = open(file_path, 'wb')
    file.write(base64.b64decode(b64s))
    file.close()

    return convertImageToJSON(file_path)


@app.route('/setdiagram', methods=['POST'])
def set_diagram():
    global diagram
    diagram = request.form['data']
    return "done"


@app.route('/getdiagram')
def get_diagram():
    global diagram
    return diagram



app.run(debug=False, host='0.0.0.0', port='5000')
