from gdo.base.util.href import href
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.file.GDT_File import GDT_File


class set_avatar(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return ''

    def gdo_needs_authentication(self) -> bool:
        return True

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_File('id').display_only().not_null().images(),
        ]

    def gdo_execute(self) -> GDT:
        image = self.param_value('id')[0]
        self._env_user.save_setting('avatar_file', image.get_id())
        return self.redirect_msg(
            href('user', 'profile', f'&for={self._env_user.render_name()}'),
            'msg_avatar_set',
        )
