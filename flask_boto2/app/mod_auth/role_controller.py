from app import db

from app.mod_auth.models import Role


class RoleController(Role):
    """
    Used to handle Role's model transactions to database
    """

    def __init__(self, name):
        self.role = Role(name)

    def create_role(self):
        try:
            db.session.add(self)
            db.session.commit()

            return self.role

        except Exception as e:
            return e, 500

    @staticmethod
    def get_role_by_name(name):
        role_instance = Role.query.filter_by(name=name).first()
        return role_instance
