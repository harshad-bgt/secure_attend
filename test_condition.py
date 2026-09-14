import enum

class RoleName(str, enum.Enum):
    ADMIN = "ADMIN"
    FACULTY = "FACULTY"

class Role:
    def __init__(self, name):
        self.name = name

class User:
    def __init__(self, id, role_name):
        self.id = id
        self.role = Role(role_name)

current_user = User(364, RoleName.FACULTY)
user_id = 364

print(current_user.role.name == RoleName.FACULTY)
print(user_id != current_user.id)
print(current_user.role.name == RoleName.FACULTY and user_id != current_user.id)
