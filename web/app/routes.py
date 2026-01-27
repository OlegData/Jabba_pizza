from web.app.home import home_route


def register_routes(app):
    app.include_router(home_route.router, prefix="", tags=["home"])
