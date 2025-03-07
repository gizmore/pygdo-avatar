from gdo.avatar.GDT_Avatar import GDT_Avatar
from gdo.form.GDT_Form import GDT_Form
from gdo.form.MethodForm import MethodForm


class set_avatar(MethodForm):

    def gdo_trigger(self) -> str:
        return ''

    def gdo_create_form(self, form: GDT_Form) -> None:
        form.add_field(
            GDT_Avatar('id'),
        )
        super().gdo_create_form(form)