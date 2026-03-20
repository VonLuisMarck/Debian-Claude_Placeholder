"""Flask API for the phishing trainer frontend."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify, render_template_string, request
from phishing_trainer import EmailGenerator, list_scenarios
from phishing_trainer.templates import get_template

app = Flask(__name__)
gen = EmailGenerator()

HTML = open(os.path.join(os.path.dirname(__file__), "frontend/index.html")).read()

@app.get("/")
def index():
    return render_template_string(HTML)

@app.get("/api/scenarios")
def scenarios():
    return jsonify(list_scenarios())

@app.get("/api/scenario/<scenario>/links")
def scenario_links(scenario):
    """Return the default link placeholders for a scenario."""
    template = get_template(scenario)
    if not template:
        return jsonify({"error": "not found"}), 404
    return jsonify(template.links)

@app.post("/api/generate/<scenario>")
@app.get("/api/generate/<scenario>")
def generate(scenario):
    """Generate a training email. POST body: {"links": {"link_key": "https://..."}}"""
    custom_links = {}
    if request.method == "POST" and request.is_json:
        custom_links = request.json.get("links", {})
    try:
        return jsonify(gen.generate(scenario, custom_links or None))
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
