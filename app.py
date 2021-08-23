from flask import Flask, render_template, Response, abort, request
from capture import CameraStream
import cv2

import requests # 다운로드 관련

import os
import subprocess

import pyautogui 


def command(cmd):
    print('전달: ',cmd)

    if cmd.startswith('cd '):
        
        try:
            os.chdir(cmd[3:])
        except:
            return "찾을 수 없는 디렉토리"

        return "change directory!"
        
    else:
        content = subprocess.getstatusoutput(cmd)

        return content
        

app = Flask(__name__)




cap = CameraStream().start()



@app.route('/')
def index():

    id = request.args.get('id')

    print(id)

    if id == 'deus':
        """Video streaming home page."""
        return render_template('index.html')
    else:
        return "Wrong ID"


@app.route('/key')
def key():
    
    key = request.args.get('key')

    pyautogui.press(key)

    return "sended."


@app.route('/pos')
def mouse():
    
    mouse = request.args.get('mouse')

    x = request.args.get('x')

    y = request.args.get('y')

    button = request.args.get('button')

    if mouse == 'down':
        pyautogui.mouseDown(x=int(x), y=int(y), button=button)

    if mouse == 'up':
        pyautogui.mouseUp(x=int(x), y=int(y), button=button)



    return "sended."



@app.route('/wheel')
def wheel():
    
    wheel = request.args.get('wheel')

    x = request.args.get('x')

    y = request.args.get('y')


    if wheel == 'up':
        pyautogui.scroll(120, x=int(x), y=int(y))

    if wheel == 'down':
        pyautogui.scroll(-120, x=int(x), y=int(y))

    return "sended."



@app.route('/adv')
def advance():

    id = request.args.get('id')

    print(id)

    if id == 'deus':
        """Video streaming home page."""
        return render_template('advance.html')
    else:
        return "Wrong ID"



@app.route('/adv', methods=['POST'])
def advance_post():
    cmd = request.form['submit_text']

    
    content = command(cmd)
        
    return render_template('advance.html',CMD_OUTPUT=content)





def gen_frame():
    """Video streaming generator function."""
    while cap:
        frame = cap.read()
        convert = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n') # concate frame one by one and show result


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')





if __name__ == '__main__':
    app.run(host='0.0.0.0',port='91', threaded=True, debug=True)
