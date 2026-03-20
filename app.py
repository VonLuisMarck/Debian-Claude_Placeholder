"""API Flask mínima para el frontend de entrenamiento."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify, render_template_string
from phishing_trainer import EmailGenerator, list_scenarios

app = Flask(__name__)
gen = EmailGenerator()

HTML = open(os.path.join(os.path.dirname(__file__), "frontend/index.html")).read()

@app.get("/")
def index():
    return render_template_string(HTML)

@app.get("/api/scenarios")
def scenarios():
    return jsonify(list_scenarios())

@app.get("/api/generate/<scenario>")
def generate(scenario):
    try:
        return jsonify(gen.generate(scenario))
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
