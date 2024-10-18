from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from model import analyze_financial_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        
        data = json.load(file)
        
        results = analyze_financial_data(data)
        
        return redirect(url_for('results', result=json.dumps(results)))

    return render_template('index.html')

@app.route('/results')
def results():
    results = json.loads(request.args.get('result'))
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
