from gdo.avatar.GDO_Avatar import GDO_Avatar
from gdo.base.GDT import GDT
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_User import GDT_User
from gdo.file.MethodFile import MethodFile


class for_user(MethodFile):

    def gdo_trigger(self) -> str:
        return ''

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_User('user').not_null(),
        ]

    def get_user(self) -> GDO_User:
        return self.param_value('user')

    def gdo_execute(self) -> GDT:
        user = self.get_user()
        file = GDO_Avatar.for_user(user).get_file()
        return self.render_file(file)
