from gdo.avatar.GDT_Avatar import GDT_Avatar
from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.base.util.href import href
from gdo.core.GDO_File import GDO_File
from gdo.file.GDT_File import GDT_File
from gdo.ui.GDT_Link import GDT_Link

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gdo.ui.GDT_Page import GDT_Page


class module_avatar(GDO_Module):

    def gdo_dependencies(self) -> list:
        return [
            'file',
        ]

    async def gdo_install(self):
        if not self.cfg_default_avatar():
            file = GDO_File.from_path(self.file_path('img/default.jpeg')).save()
            self.save_config_val('default_avatar', file.get_id())

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_File('default_avatar').not_null().upload_path('module_avatar.default_avatar'),
        ]

    def cfg_default_avatar(self) -> GDO_File|None:
        avatar = self.get_config_value('default_avatar')
        return avatar[0] if avatar else None

    def gdo_user_config(self) -> list[GDT]:
        return [
            GDT_Avatar('avatar_file'),
        ]

    def gdo_user_settings(self) -> list[GDT]:
        return [
            GDT_Link('change_avatar').href(href('avatar', 'upload')).text('upload_avatar'),
        ]

    def gdo_load_scripts(self, page: 'GDT_Page'):
        self.add_css('css/pygdo-avatar.css')
