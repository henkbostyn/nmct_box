from flask import Flask
from flask import render_template
from flask import request

from model.neopixel_nmct_box import NmctPixel
from model.I2c_Lcd_nmct_box import GPIOLCD


app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/dashboard')
def show_dashboard():
    return render_template("index.html")

@app.route('/write_lcd',methods=['POST'])
def write_lcd():
    text = request.form['lcdMessage']
    text = text.rstrip("")
    #sda en scl pin meegeven
    display = GPIOLCD(5,13)
    display.lcd_write_text(text)


    return render_template("index.html",lcdMessage=text)

@app.route('/show_nmct_pixel',methods=['POST'])
def show_nmct_pixel():
    show_method = request.form['show_method']
    NmctPixel.call_method(show_method)
    return render_template("index.html",show_method=show_method)



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
