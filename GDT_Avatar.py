from gdo.base.Util import href
from gdo.core.GDO_User import GDO_User
from gdo.ui.GDT_Image import GDT_Image


class GDT_Avatar(GDT_Image):

    def __init__(self, name: str):
        super().__init__(name)

    def for_user(self, user: GDO_User):
        self.gdo(user)
        self.alternate('alt_avatar', (user.render_name(),))
        self.href(href('user', 'profile', f'&for={user.get_id()}'))
        return self
