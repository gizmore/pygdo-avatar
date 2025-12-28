from gdo.base.GDT import GDT
from gdo.file.MethodFile import MethodFile
from gdo.ui.GDT_Image import GDT_Image


class default(MethodFile):

    @classmethod
    def gdo_trigger(cls) -> str:
        return ''

    def gdo_execute(self) -> GDT:
        file = GDT_Image.module_config('avatar', 'default_avatar').get_file()[0]
        return self.render_file(file)
