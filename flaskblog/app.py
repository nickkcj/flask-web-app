from extensions import app, db, bcrypt, login_manager

def create_app():
    app.config['SECRET_KEY'] = 'a069dcf1fafbc38d6e69f8aedebd817b'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.app_context().push()
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'
    login_manager.login_message_category = 'info'

    from routes.blog_routes import routes as rt
    app.register_blueprint(rt)

    return app
