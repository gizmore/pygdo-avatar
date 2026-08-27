from gdo.avatar.GDT_Avatar import GDT_Avatar
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_Container import GDT_Container
from gdo.core.GDO_User import GDO_User
from gdo.user.GDT_ProfileLink import GDT_ProfileLink


class GDT_AvatarGallery(GDT_Container):
    """A compact, responsive collection of profile-avatar links."""

    def render_class(self) -> str:
        return 'avatar-gallery'


class GDT_AvatarTile(GDT_Container):
    """One non-interactive avatar with a profile link below it."""

    def __init__(self, user: GDO_User):
        super().__init__()
        self.vertical()
        self.add_field(GDT_Avatar('avatar').for_user(user))
        self.add_field(GDT_ProfileLink().user(user))

    def render_class(self) -> str:
        return 'gdt-col avatar-gallery-tile'


class gallery(Method):
    """Show users who explicitly selected an avatar other than the default."""

    def gdo_connectors(self) -> str:
        return 'web'

    def get_users(self) -> list[GDO_User]:
        query = GDO_User.table().select()
        GDO_User.join_setting(query, 'avatar_file')
        default_id = GDT_Avatar.get_default_id()
        query.where(
            "setting_avatar_file.uset_val IS NOT NULL "
            "AND setting_avatar_file.uset_val != '' "
            f"AND setting_avatar_file.uset_val != {GDT.quote(default_id)}"
        ).order('gdo_user.user_name ASC')
        return query.exec()

    def gdo_execute(self) -> GDT:
        out = GDT_AvatarGallery()
        for user in self.get_users():
            out.add_field(GDT_AvatarTile(user))
        return out
