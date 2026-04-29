from flask import Blueprint
from utils.response_utils import success
from services.embedding_service import get_model

health_bp = Blueprint("health", __name__)


@health_bp.route("/health")
def health():
    return success({"model_loaded": get_model() is not None, "version": "1.0.0"})
