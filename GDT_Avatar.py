from gdo.base.util.href import href
from gdo.core.GDO_User import GDO_User
from gdo.ui.GDT_Image import GDT_Image


class GDT_Avatar(GDT_Image):

    def __init__(self, name: str):
        super().__init__(name)

    def for_user(self, user: GDO_User):
        self.gdo(user)
        self.alternate('alt_avatar', (user.render_name(),))
        self.href(href('avatar', 'for_user', f'&id={user.get_id()}'))
        return self

    def render_card(self) -> str:
        return self.render_html()
    