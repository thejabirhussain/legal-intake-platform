import asyncio
import bcrypt
# Monkey patch for passlib + bcrypt compatibility
if not hasattr(bcrypt, "__about__"):
    try:
        bcrypt.__about__ = type("about", (object,), {"__version__": bcrypt.__version__})
    except AttributeError:
        bcrypt.__about__ = type("about", (object,), {"__version__": "4.0.1"})

from app.core import security
from app.core.database import AsyncSessionLocal
from app.models.all_models import User
from app.schemas.user import UserRole
from sqlalchemy import select

async def create_initial_user():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).filter(User.email == "user@example.com"))
        user = result.scalars().first()
        
        if not user:
            print("Creating initial user...")
            hashed_password = security.get_password_hash("password")
            new_user = User(
                email="user@example.com",
                hashed_password=hashed_password,
                role=UserRole.SENIOR_LAWYER,
                is_active=True,
                full_name="Senior Partner"
            )
            db.add(new_user)
            await db.commit()
            print("User created: user@example.com / password")
        else:
            print("User already exists.")

if __name__ == "__main__":
    asyncio.run(create_initial_user())
