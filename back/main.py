from flask import Flask
from flask import jsonify
from flask_cors import CORS
from back.solver import Solver

app = Flask(__name__)
CORS(app)

solver = Solver()


@app.route("/projects")
def get_projects():
    return jsonify(solver.fetcher.projects)
    
    
@app.route("/persons/<project_id>/<months>")
def projects(project_id, months):
    return jsonify(solver.get_persons(project_id, int(months)))


@app.route("/projects/load")
def load_projects():
    solver.fetcher.load_cookies_and_projects()
    return jsonify(solver.fetcher.projects)


@app.route("/define_croissanists/<project_id>/<months>/<nb_croissanist>")
def define_croissanists(project_id, months, nb_croissanist):
    croissanists = solver.define_croissanists(project_id, int(months), int(nb_croissanist))
    return jsonify(croissanists)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
