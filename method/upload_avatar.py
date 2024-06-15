from gdo.file.GDT_FileUpload import GDT_FileUpload
from gdo.form.GDT_Form import GDT_Form
from gdo.form.MethodForm import MethodForm


class upload_avatar(MethodForm):

    def gdo_create_form(self, form: GDT_Form) -> None:
        form.add_field(
            GDT_FileUpload('image').not_null(),
        )
        super().gdo_create_form(form)

    def form_submitted(self):
        return self.msg('msg_avatar_uploaded')
