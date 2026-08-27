from functools import lru_cache

from gdo.base.Trans import t
from gdo.base.util.href import href
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Template import GDT_Template
from gdo.ui.GDT_Image import GDT_Image


class GDT_Avatar(GDT_Image):

    def __init__(self, name: str):
        super().__init__(name)

    def for_user(self, user: GDO_User):
        self.gdo(user)
        self.val(user.get_setting_val('avatar_file'))
        self.alternate('alt_avatar', (user.render_name(),))
        self.href(href('avatar', 'for_user', f'&id={user.get_id()}&file={self.get_val()}'))
        return self

    def is_filterable(self) -> bool:
        return False

    @classmethod
    @lru_cache(maxsize=None)
    def get_default_id(cls):
        return GDT_Image.module_config('avatar', 'default_avatar').get_val()

    def html_gender_class(self):
        gender = self._gdo.get_setting_val('gender')
        return '' if not gender else gender

    def href_render(self):
        uid = self._gdo.get_id()
        if val := self.get_val():
            return href('avatar', 'for_user', f'&user={uid}&file={val}')
        else:
            return href('avatar', 'default', f'&file={self.get_default_id()}')

    def alt_text(self) -> str:
        return t('alt_avatar', (self._gdo.render_name(),))

    def render_card(self) -> str:
        return self.render_html()

    def render_html(self) -> str:
        classes = f'gdo-avatar {self.html_gender_class()} {self.get_attrs().get("class", "")}'.strip()
        return f'<span class="{classes}"><img src="{self.href_render()}" alt="{self.alt_text()}"></span>'

    def render_cell(self) -> str:
        return self.render_html()
