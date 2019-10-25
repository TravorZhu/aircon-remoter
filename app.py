import json

from flask import Flask, request
from py_irsend import irsend

app = Flask(__name__, static_url_path='', static_folder='./static')

direct_dict = ['s', 'a']
speed_dict = ['a', 'w', 'm', 's']

status = {'tem': 25, 'direct': 1, 'speed': 1, 'is_open': 1}


@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


@app.route('/status', methods=['POST'])
def change_status():
    # print(request.get_data())
    new_status=json.loads(request.get_data().decode())
    # print(new_status)
    tem = new_status['tem']
    direct = new_status['direct']
    speed = new_status['speed']
    status['tem']=tem
    status['direct']=direct
    status['speed']=speed
    # print(tem, direct, speed)
    send_str = '{}C{}{}'.format(tem, speed_dict[speed], direct_dict[direct])
    print('send_str:', send_str)
    irsend.send_once('aircon', [send_str])
    status['is_open']=1
    return json.dumps(status)


@app.route('/status', methods=['GET'])
def getstatus():
    return json.dumps(status)

@app.route('/power_off',methods=['POST'])
def poweroff():
    irsend.send_once('aircon',['off'])
    status['is_open']=0
    return 'ok'


if __name__ == '__main__':
    irsend.send_once('aircon',
                     ['{}C{}{}'.format(status['tem'], speed_dict[status['speed']], direct_dict[status['direct']])])
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)
