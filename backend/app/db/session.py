from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

_engine = None
_SessionFactory = None


def get_engine():
    global _engine
    if _engine is None:
        # pool_pre_ping: Neon suspends its compute after a period of
        # inactivity and drops idle connections, which otherwise surfaces as
        # "SSL connection has been closed unexpectedly" on the first query
        # after a lull. pre_ping tests each pooled connection before use and
        # transparently reconnects if it's gone dead.
        _engine = create_engine(get_settings().database_url, pool_pre_ping=True)
    return _engine


def get_session() -> Session:
    global _SessionFactory
    if _SessionFactory is None:
        _SessionFactory = sessionmaker(bind=get_engine())
    return _SessionFactory()
