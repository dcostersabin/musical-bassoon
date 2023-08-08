from flask.views import MethodView
from flask import jsonify


class HealthCheckView(MethodView):
    def get(self):
        return jsonify({"status": "If You See This The Server Is Healthy"})
