from data.user_data import UserData


class UserService:
    def __init__(self, user_data: UserData):
        self.user_data = user_data
