from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task

microblogapp = create_app()
cli.register(microblogapp)


@microblogapp.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notifications, 'Task': Task}