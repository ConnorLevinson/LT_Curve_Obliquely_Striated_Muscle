from flask import Flask, render_template, request
import model
import io
import base64
from matplotlib.figure import Figure

app = Flask(__name__, static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        angle = float(request.form['angle'])
        A = float(request.form['A'])
        I = float(request.form['I'])
        BZ = float(request.form['BZ'])
        
        data = model.sarc_sim(angle, False, A, I, BZ)

        fig = Figure()
        ax = fig.subplots()
        ax.plot(data[:, 0], data[:, 1])
        ax.set_xlabel('Sarcomere Length')
        ax.set_ylabel('Tension')
        ax.set_title('Tension vs. Sarcomere Length')
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return render_template("index.html", result="data:image/png;base64,{}".format(data))

    else:
        return render_template("index.html")

@app.route('/generate_graph', methods=['GET', 'POST'])
def generate_graph():
    if request.method == 'GET':
        angle = float(request.args.get('angle'))
        A = float(request.args.get('A'))
        I = float(request.args.get('I'))
        BZ = float(request.args.get('BZ'))
        
        data = model.sarc_sim(angle, False, A, I, BZ)

        fig = Figure()
        ax = fig.subplots()
        ax.plot(data[:, 0], data[:, 1])
        ax.set_xlabel('Sarcomere Length')
        ax.set_ylabel('Tension')
        ax.set_title('Tension vs. Sarcomere Length')
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return render_template("index.html", result="data:image/png;base64,{}".format(data))

    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
