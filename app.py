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
        
        # Assuming your model function can now receive these parameters
        data = model.sarc_sim(angle, False, A, I, BZ)

        # Generate the plot
        fig = Figure()
        ax = fig.subplots()
        ax.plot(data[:, 0], data[:, 1])
        ax.set_xlabel('Sarcomere Length')
        ax.set_ylabel('Tension')
        ax.set_title('Tension vs. Sarcomere Length')
        
        # Save it to a temporary buffer.
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return render_template("index.html", result="data:image/png;base64,{}".format(data))

    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
