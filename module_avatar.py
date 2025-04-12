from gdo.avatar.GDO_Avatar import GDO_Avatar
from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.base.Util import href
from gdo.core.GDO_File import GDO_File
from gdo.file.GDT_File import GDT_File
from gdo.ui.GDT_Link import GDT_Link


class module_avatar(GDO_Module):

    def gdo_dependencies(self) -> list:
        return [
            'file',
        ]

    def gdo_classes(self):
        return [
            GDO_Avatar,
        ]

    def gdo_install(self):
        if not self.cfg_default_avatar():
            file = GDO_File.from_path(self.file_path('img/default.jpeg')).save()
            self.save_config_val('default_avatar', file.get_id())

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_File('default_avatar').not_null().upload_path('module_avatar.default_avatar'),
        ]

    def cfg_default_avatar(self) -> GDO_File:
        return self.get_config_value('default_avatar')[0]

    def gdo_user_settings(self) -> list[GDT]:
        return [
            GDT_Link().href(href('avatar', 'upload')).text('upload_avatar'),
        ]