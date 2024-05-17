from dataclasses import dataclass


@dataclass
class Admin:
    name: str
    password: str

    def verify_password(self, password_str: str):
        return password_str == self.password
