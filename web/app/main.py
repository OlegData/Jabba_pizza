import argparse
import logging

import structlog
import uvicorn
from fastapi import FastAPI
from web.app.routes import register_routes


def log_config():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )


def create_app():
    app = FastAPI()
    register_routes(app)
    return app


app = create_app()


def main():
    parser = argparse.ArgumentParser(description="Run the Jabbas Pizza web app")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run locally with reload on and localhost binding",
    )
    args = parser.parse_args()

    log_config()
    logger = structlog.get_logger()
    logger.info("Starting application")
    host = "127.0.0.1" if args.debug else "0.0.0.0"
    uvicorn.run(
        "web.app.main:app",
        host=host,
        port=8000,
        reload=args.debug,
    )
    logger.info("Application started successfully")


if __name__ == "__main__":
    main()
