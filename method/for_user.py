from gdo.base.GDT import GDT
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_User import GDT_User
from gdo.file.MethodFile import MethodFile


class for_user(MethodFile):

    @classmethod
    def gdo_trigger(cls) -> str:
        return ''

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_User('user').not_null(),
        ]

    def get_user(self) -> GDO_User:
        return self.param_value('user')

    def gdo_execute(self) -> GDT:
        user = self.get_user()
        file = user.get_setting_value('avatar_file')[0]
        return self.render_file(file)
