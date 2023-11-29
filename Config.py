import uuid

from flask import Flask
from datetime import datetime, date
from flask.json.provider import DefaultJSONProvider
from flask_restful.reqparse import text_type
from flask_sqlalchemy import SQLAlchemy
from werkzeug.http import http_date
from models.db import Config


class JSONEncoder(DefaultJSONProvider):
    """The default Flask JSON encoder.  This one extends the default simplejson
    encoder by also supporting ``datetime`` objects, ``UUID`` as well as
    ``Markup`` objects which are serialized as RFC 822 datetime strings (same
    as the HTTP date format).  In order to support more data types override the
    :meth:`default` method.
    """

    def default(self, o):
        """Implement this method in a subclass such that it returns a
        serializable object for ``o``, or calls the base implementation (to
        raise a :exc:`TypeError`).

        For example, to support arbitrary iterators, you could implement
        default like this::

            def default(self, o):
                try:
                    iterable = iter(o)
                except TypeError:
                    pass
                else:
                    return list(iterable)
                return JSONEncoder.default(self, o)
        """
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, datetime):
            return http_date(o.utctimetuple())
        if isinstance(o, date):
            return http_date(o.timetuple())
        if isinstance(o, uuid.UUID):
            return str(o)
        if hasattr(o, '__html__'):
            return text_type(o.__html__())
        return super().default(o)


app = Flask(__name__)
app.config.from_object(Config)
app.json = JSONEncoder(app)
db = SQLAlchemy(app)
