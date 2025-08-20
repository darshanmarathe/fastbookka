from fastapi import APIRouter, HTTPException, status
from typing import List

from tomlkit import datetime
from models.user import User, UserLogin
from repositories.userrepo import UserRepository
from datetime import datetime
from passlib.context import CryptContext  # type: ignore


class UserController:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["users"])
        self.setup_routes()
        self.userRepo = UserRepository()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def setup_routes(self):
        self.router.get("/")(self.index)
        self.router.get("/{id}")(self.show)
        self.router.post("/")(self.store)
        self.router.post("/login")(self.login)
        # self.router.put("/{id}/password")(self.change_password)
        # self.router.put("/{id}")(self.update)
        # self.router.delete("/{id}")(self.destroy)

    def index(self) -> List[User]:
        return self.userRepo.get_all_users()

    def show(self, id: int) -> User:
        user = self.userRepo.get_user(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    def store(self, user: User) -> User:
        # Strong password check
        if (
            len(user.password) < 8
            or not any(c.isdigit() for c in user.password)
            or not any(c.isupper() for c in user.password)
            or not any(c.islower() for c in user.password)
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long and contain upper, lower case letters and digits.",
            )
        # Duplicate username check
        if self.userRepo.check_user_or_email_exists(user.username, user.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists.",
            )
        user.password = self.pwd_context.hash(user.password)
        user.createdAt = datetime.now()
        new_user = self.userRepo.add_user(user)
        return new_user

    def login(self, user: UserLogin) -> User:
        db_user = self.userRepo.get_user_by_username(user.username)
        print(user, db_user)
        if not db_user or not self.pwd_context.verify(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        return user

    # def change_password(
    #     self, username: str, old_password: str, new_password: str
    # ) -> bool:
    #     user = self.userRepo.get_user_by_username(username)
    #     if not user or not self.pwd_context.verify(old_password, user.password):
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    #         )
    #     user.password = self.pwd_context.hash(new_password)
    #     return self.userRepo.update_user(id, user)

    # def update(self, id: int, user: User) -> User:
    #     existing = self.userRepo.get_user(id)
    #     if not existing:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    #         )
    #     # Don't update password here
    #     user.password = existing.password
    #     updated = self.userRepo.update_user(id, user)
    #     if not updated:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST, detail="Update failed"
    #         )
    #     return self.userRepo.get_user(id)

    # def destroy(self, id: int) -> User:
    #     user = self.userRepo.get_user(id)
    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    #         )
    #     self.userRepo.delete_user(id)
    #     return user
