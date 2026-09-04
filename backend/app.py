import os

from flask import Flask

from config import config

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend", "templates")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend", "static")


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR,
    )
    app.secret_key = config.SECRET_KEY

    from routes.pipeline import bp as pipeline_bp
    from routes.applications import bp as applications_bp
    from routes.showings import bp as showings_bp
    from routes.tickets import bp as tickets_bp
    from routes.applicant import bp as applicant_bp
    from routes.stub import bp as stub_bp
    from routes.sms import bp as sms_bp

    app.register_blueprint(pipeline_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(showings_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(applicant_bp)
    app.register_blueprint(stub_bp)
    app.register_blueprint(sms_bp)

    @app.context_processor
    def inject_globals():
        return {"airtable_configured": config.airtable_configured}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
