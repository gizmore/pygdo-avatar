from gdo.core.GDO_User import GDO_User
from gdo.core.WithGDO import WithGDO
from gdo.ui.GDT_Image import GDT_Image


class GDT_Avatar(WithGDO, GDT_Image):

    def for_user(self, user: GDO_User):
        self.gdo(user)
        self.alternate('alt_avatar', [user.render_name()])
        return self
