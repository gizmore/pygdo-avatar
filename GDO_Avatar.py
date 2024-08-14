from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.Trans import t
from gdo.base.Util import href
from gdo.core.GDO_File import GDO_File
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Template import GDT_Template
from gdo.core.GDT_User import GDT_User
from gdo.date.GDT_Created import GDT_Created
from gdo.file.GDT_File import GDT_File


class GDO_Avatar(GDO):

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_User('avatar_user').primary().not_null(),
            GDT_File('avatar_file').not_null(),
            GDT_Created('avatar_created'),
        ]

    def get_user(self) -> GDO_User:
        return self.gdo_value('avatar_user')

    def get_file(self) -> GDO_File:
        return self.gdo_value('avatar_file')

    @classmethod
    def for_user(cls, user: GDO_User):
        if avatar := cls.table().get_by_id(user.get_id()):
            return avatar
        return cls.default_avatar(user)

    @classmethod
    def default_avatar(cls, user: GDO_User):
        from gdo.avatar.module_avatar import module_avatar
        return cls.blank({
            'avatar_user': user.get_id(),
            'avatar_file': module_avatar.instance().cfg_default_avatar().get_id(),
        })

    ##########
    # Render #
    ##########

    def href_render(self):
        uid = self.get_user().get_id()
        return href('avatar', 'for_user', f'&user={uid}')

    def alt_text(self) -> str:
        return t('avatar_alt_text', [self.get_user().render_name()])

    def html_gender_class(self):
        gender = self.get_user().get_setting_val('gender')
        if not gender:
            return ''
        return f'gdo-avatar-{gender}'

    def render_html(self) -> str:
        return GDT_Template.python('avatar', 'avatar.html', {'avatar': self})


