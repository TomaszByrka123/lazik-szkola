import time
from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

import com

#polaczenie z mqtt z biblioteki com
broker_address = "192.168.8.125"
try:
    client = com.mqtt.Client()
    client.on_connect = com.on_connect
    client.on_message = com.on_message

    client.connect(broker_address, 1883, 60)
    client.loop_start()
except:
    print("bład przy łączeniu z raspberry pi")



#Stworzenie stron wszystkich zakładek

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/czujnik')
def czujnik():
    return render_template('czujnik.html')

@app.route('/kamery')
def kamery():
    return render_template('kamery.html')

@app.route('/lokalizacja')
def lokalizacja():
    return render_template('lokalizacja.html')

@app.route('/sterowanie')
def sterowanie():
    return render_template('sterowanie.html')

@app.route('/ustawienia')
def ustawienia():
    return render_template('ustawienia.html')

@app.route('/science')
def science():
    return render_template('science.html')


def data_from_raspberry():
    count = com.get_last_value()
    while True:
        count = com.get_last_value()
        if count is not None:
            yield f'data: {count[0]}\n\n'
        time.sleep(1)

#publikowanie na /stream danych [0] z tabeli z raspberry pi
@app.route('/stream')
def stream():
    return Response(data_from_raspberry(), mimetype='text/event-stream')



if __name__ == '__main__':
    app.run(debug=True)
