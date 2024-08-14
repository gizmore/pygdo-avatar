from gdo.avatar.GDO_Avatar import GDO_Avatar
from gdo.core.GDT_String import GDT_String
from gdo.file.GDT_File import GDT_File
from gdo.form.GDT_Form import GDT_Form
from gdo.form.MethodForm import MethodForm


class upload(MethodForm):

    def gdo_trigger(self) -> str:
        return ''

    def gdo_create_form(self, form: GDT_Form) -> None:
        form.add_field(
            GDT_String('test'),
            GDT_File('image').not_null().images(),
        )
        super().gdo_create_form(form)

    def form_submitted(self):
        image = self.param_value('image')
        image.save()

        GDO_Avatar.blank({
            'avatar_user': self._env_user.get_id(),
            'avatar_file': image.get_id(),
        }).insert()

        return self.msg('msg_avatar_uploaded')
