from gdo.base.util.href import href
from gdo.file.GDT_File import GDT_File
from gdo.form.GDT_Form import GDT_Form
from gdo.form.MethodForm import MethodForm


class upload(MethodForm):

    @classmethod
    def gdo_trigger(cls) -> str:
        return ''

    def gdo_create_form(self, form: GDT_Form) -> None:
        form.add_field(
            GDT_File('image').not_null().images(),
        )
        super().gdo_create_form(form)

    def form_submitted(self):
        image = self.param_value('image')[0]
        self._env_user.save_setting('avatar_file', image.get_id())
        return self.redirect_msg(
            href('user', 'profile', f'&for={self._env_user.render_name()}'),
            'msg_avatar_uploaded',
        )
