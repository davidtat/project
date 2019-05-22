import os
import web
import string
import random
import datetime
from jinja2 import Environment,FileSystemLoader

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from createtable import *

from dodotable.schema import Table, Column
engine = create_engine('sqlite:///user.db', echo=True)
# create a Session
Session = sessionmaker(bind=engine)
session = Session()

urls = (
    "/", "home",
    "/add", "add",
    "/view", "view"
    )

app = web.application(urls, globals())


def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    #jinja_env.update_template_context(context)
    return jinja_env.get_template(template_name).render(context)

class home:
    def GET(self):
        # You can use a relative path as template name, for example, 'ldap/hello.html'.
        return render_template('home.html', name='home')


class add:
    def GET(self):
        web.header('Content-type', 'text/html')
        uname = "".join(random.choice(string.letters) for i in range(5))
        fname = "".join(random.choice(string.letters) for i in range(3))
        lname = "".join(random.choice(string.letters) for i in range(3))
        passw = random.randint(1,9999)
        user = User(uname,fname,lname,passw)
        session.add(user)
        session.commit()
        return render_template('add.html',uname=uname, fname=fname, lname=lname, passw=passw)

class view:
    def GET(self):
        web.header('Content-type', 'text/html')
        table=session.query(User).all()
        return render_template('view.html',user=table)

if __name__ == "__main__":
    app.run()