import os
from flask import Flask
from src.utils.db_utils import db, init_db
from src.utils.celery_utils import make_celery
from flasgger import Swagger
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Import Blueprints
from src.api.event import event_bp
from src.api.ticket import ticket_bp
from src.api.user import user_bp


jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config["TZ"] = "UTC"

    # 🔐 JWT Configuration
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))

    # Database / Celery / Swagger Config
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@db:5432/events_db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CELERY_BROKER_URL="redis://redis:6379/0",
        CELERY_RESULT_BACKEND="redis://redis:6379/0",
        SWAGGER={
            "title": "Event Ticketing API",
            "uiversion": 3,
        }
    )

    # Initialize extensions
    init_db(app)
    migrate = Migrate(app, db)
    celery = make_celery(app)
    jwt.init_app(app) 

    Swagger(app)

    # Register blueprints
    app.register_blueprint(event_bp, url_prefix="/api/events")
    app.register_blueprint(ticket_bp, url_prefix="/api/tickets")
    app.register_blueprint(user_bp, url_prefix="/api/users")

    return app, celery


app, celery = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)