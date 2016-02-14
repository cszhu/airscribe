from flask import Flask,request
import airscribe as air
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)

app.debug = True

@app.route('/give_text', methods=['POST'])
def give_text():
    if not request.json or not 'text' in request.json:
        return "no thanks bae :'("
    text =  request.json['text']
    print 'Recieved Text:'
    print text
    # text = open('input.txt', 'r').read() # Temp to test on input
    analyzed = air.analyze(text)
    print "Returning Text:"
    print analyzed
    out = open('out.txt', 'w').write(analyzed)
    return analyzed

@app.route('/')
def home():
    return "baebae bae"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
