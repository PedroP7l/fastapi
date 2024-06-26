from sqlalchemy import select

from fast_api.models import User


def test_create_user(session):
    user = User(username='pedro', email='pedro@paulo.com', password='senha')
    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'pedro@paulo.com')
    )
    assert result.username == 'pedro'
