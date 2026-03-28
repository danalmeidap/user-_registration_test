from sqlalchemy.orm import Session

from fast_api_zero.database import engine, get_session


def test_engine_should_be_initialized():
    assert engine is not None
    assert str(engine.url).endswith('database.db')


def test_get_session_should_yield_session():
    session_generator = get_session()
    session = next(session_generator)

    try:
        assert isinstance(session, Session)
        assert session.is_active
    finally:
        try:
            next(session_generator)
        except StopIteration:
            pass
