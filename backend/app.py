"""
DebugMind - AI Code Debugging Assistant
Flask Backend Entry Point
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_service import debug_code
import logging

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# App
app = Flask(__name__)
CORS(app)


# Routes

@app.route("/health", methods=["GET"])
def health():
    """Simple health-check endpoint."""
    return jsonify({"status": "ok", "service": "DebugMind API"}), 200


@app.route("/debug", methods=["POST"])
def debug():
    """
    POST /debug
    Body (JSON):
        code     : str  – the code snippet to debug (required)
        error    : str  – optional error message / traceback
        language : str  – programming language (default: "Python")
    Returns:
        JSON with keys: error_summary, root_cause, explanation,
                        fixed_code, optimizations
    """
    payload = request.get_json(silent=True)

    if not payload:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    code = (payload.get("code") or "").strip()
    if not code:
        return jsonify({"error": "Field 'code' is required and cannot be empty."}), 400

    error_msg = (payload.get("error") or "").strip()
    language  = (payload.get("language") or "Python").strip()

    logger.info("Debugging request — language: %s | error provided: %s", language, bool(error_msg))

    result = debug_code(code=code, error_msg=error_msg, language=language)

    if "error" in result:
        logger.error("AI service error: %s", result["error"])
        return jsonify(result), 500

    return jsonify(result), 200


# Run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)