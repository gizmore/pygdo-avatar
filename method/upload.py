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
        image.save()
        self._env_user.save_setting('avatar_file', image.get_id())
        self.msg('msg_avatar_uploaded')
        return self.redirect(href('avatar', 'set_avatar', f"&id={image.get_id()}"), 'msg_avatar_uploaded')
