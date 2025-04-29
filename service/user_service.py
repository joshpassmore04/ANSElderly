from typing import Optional

from werkzeug.security import generate_password_hash, check_password_hash

import orm
from data.permission import PermissionType, PermissionResult, RolePermissions
from data.schema.user import UserOut
from data.user_data import UserData
from orm.user.permission import Permission
from orm.user.user import User


class UserService:
    def __init__(self, user_data: UserData):
        self.user_data = user_data
    def register_user(self, first_name: str, last_name: str, email: str, password: str) -> Optional[UserOut]:
        existing_user = self.user_data.get_user_by_email(email)
        if existing_user is None:
            created_user =  self.user_data.create_user(first_name=first_name, last_name=last_name, email=email, hashed_password=generate_password_hash(password))
            return created_user
        return None
    def validate_login(self, email: str, password: str) -> Optional[UserOut]:
        user = self.user_data.validate_user_by_email(email)
        print("1")
        if user is not None:
            if check_password_hash(user.hashed_password, password) and email == user.email:
                return UserOut.model_validate(user)
        return None
    def get_user_by_id(self, user_id: int) -> Optional[UserOut]:
        return self.user_data.get_user_by_id(user_id)
    def get_traveller_by_id(self, traveller_id: int) -> Optional[User]:
        return self.user_data.get_traveller_by_id(traveller_id)
    def delete_user_by_id(self, user_id: int) -> bool:
        return self.user_data.delete_user_by_id(user_id)
    def give_permission_from(self, from_user_id: int, to_user_id: int, permission: PermissionType) -> PermissionResult:
        user = self.user_data.get_user_by_id(from_user_id)
        if user:
            if self.has_permission(from_user_id, PermissionType.CAN_UPDATE_OTHERS_PERMISSIONS):
                return self.give_permission(to_user_id, permission)
            return PermissionResult.FAILED
        return PermissionResult.FAILED
    def give_permission(self, to_user_id: int, permission: PermissionType) -> PermissionResult:
        if not self.has_permission(to_user_id, permission):
            return self.user_data.give_permission(to_user_id, permission)
        else:
            return PermissionResult.EXISTS
    def remove_permission_from(self, from_user_id: int, to_user_id: int, permission: PermissionType) -> bool:
        user = self.user_data.get_user_by_id(from_user_id)
        if user:
            if self.has_permission(from_user_id, PermissionType.CAN_UPDATE_OTHERS_PERMISSIONS):
                return self.remove_permission(to_user_id, permission)
            return False
        return False
    def remove_permission(self, user_id: int, permission: PermissionType) -> bool:
        return self.user_data.remove_permission(user_id, permission)
    def has_permission(self, user_id: int, permission: PermissionType) -> bool:
        return self.user_data.has_permission(user_id, permission)
    def set_role_from(self, from_user_id: int, to_user_id: int, role: RolePermissions) -> bool:
        user = self.user_data.get_user_by_id(from_user_id)
        if user:
            if self.has_permission(from_user_id, PermissionType.CAN_UPDATE_OTHERS_ROLES):
                return self.set_role(to_user_id, role)
            else:
                return False
        else:
            return False
    def set_role(self, user_id: int, role: RolePermissions) -> bool:
        return self.user_data.set_role(user_id, role.label)
    def has_role(self, user_id: int, role: RolePermissions) -> bool:
        return self.user_data.has_role(user_id, role.label)
    def promote_user(self, user_id: int, role: RolePermissions) -> bool:
        worked = self.set_role(user_id, role)
        if worked:
            for permission in role.permissions:
                self.give_permission(user_id, permission)
        return worked


