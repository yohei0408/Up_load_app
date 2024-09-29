from flask import Flask, render_template, request, redirect
import io
from PIL import Image
import base64

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png','jpg','gif','jpeg'])

def allwed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET', 'POST'])
def predicts():

    if request.method == 'POST':
        if 'filename' not in request.files:
            return redirect(request.url)
        file = request.files['filename']
        if file and allwed_file(file.filename):

            buf = io.BytesIO()
            image = Image.open(file).convert('RGB')
            image.save(buf, 'png')
            base64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
            base64_data = 'data:image/png;base64,{}'.format(base64_str)
            message_ = '画像がアップロードされました。'
            return render_template('result.html', message=message_, image=base64_data)
        return redirect(request.url)
    elif request.method == 'GET':
        return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)