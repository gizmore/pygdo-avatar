import os

from gdo.avatar.GDT_Avatar import GDT_Avatar
from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.base.Util import module_enabled
from gdo.core.GDO_File import GDO_File
from gdo.core.GDO_UserSetting import GDO_UserSetting
from gdo.core.GDO_Session import GDO_Session
from gdo.core.connector.Web import Web
from gdotest.TestUtil import web_plug, reinstall_module, web_gizmore, install_module, GDOTestCase


class AvatarTest(GDOTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        Application.init_cli()
        install_module('avatar')
        loader = ModuleLoader.instance()
        loader.load_modules_db()
        loader.init_modules(True, load_vals=True)
        loader.init_cli()
        Application.set_session(GDO_Session.for_user(web_gizmore()))

    def test_00_install(self):
        reinstall_module('avatar')
        self.assertTrue(module_enabled('avatar'), 'cannot install avatar')

    def test_01_upload_form(self):
        out = web_plug('avatar.upload.html').exec()
        self.assertIn('image', out, 'Avatar upload file is not rendered.')

    def test_02_render(self):
        avatar = GDT_Avatar('a').for_user(web_gizmore())
        out = avatar.render_html()
        self.assertIn('avatar', out, 'cannot render avatar.')

    def test_03_upload_text(self):
        web_plug('core.whoami.html').exec()
        data = b'-----------------------------283687824923932629242982017982\r\nContent-Disposition: form-data; name=\"test\"\r\n\r\ngjgjgj\r\n-----------------------------283687824923932629242982017982\r\nContent-Disposition: form-data; name=\"image\"; filename=\"AnschreibenAndrena.txt\"\r\nContent-Type: text/plain\r\n\r\nHallo,\n\nIch bewerbe mich f\\xc3\\xbcr eine Anstellung als Programmierer,\n\nIch heisse Christian, bin 43 Jahre alt, und komme aus Peine, Niedersachsen.\n\nIch spreche einige Programmiersprachen fliessend, darunter PHP, Java, Jacascript, Python, Ruby und C.\n\nIm Design bin ich nicht der beste, kann aber Anforderungen in CSS umsetzen.\n\nIch bin der Kopf und Programmierer hinter www.wechall.net und kenne mich auch in Datenbanken etwas aus.\n\nMeherer GB CSV streame ich zum Fr\\xc3\\xbchst\\xc3\\xbcck ^^\n\nIch hoffe ich habe interesse geweckt.\n\nViele Gr\\xc3\\xbc\\xc3\\x9fe\nChristian Busch\ngizmore@wechall.net\n\n\r\n-----------------------------283687824923932629242982017982\r\nContent-Disposition: form-data; name=\"csrf\"\r\n\r\n243e71619862\r\n-----------------------------283687824923932629242982017982\r\nContent-Disposition: form-data; name=\"submit\"\r\n\r\nSubmit\r\n-----------------------------283687824923932629242982017982--\r\n'
        out = web_plug('avatar.upload.html').post_multipart(data, '---------------------------283687824923932629242982017982').exec()
        self.assertIn('file format text/plain is not supported', out, 'Can upload text file to avatars.')

    def test_04_avatar_renders_the_users_saved_file(self):
        user = web_gizmore()
        user.save_setting('avatar_file', '123')
        avatar = GDT_Avatar('avatar').for_user(user)
        self.assertIn('file.123', avatar.render_html())

    def test_05_set_avatar_saves_the_selected_image(self):
        user = web_gizmore()
        file = GDO_File.from_path(Application.file_path('gdo/avatar/img/default.jpeg')).save()
        out = web_plug(f'avatar.set_avatar.html?_lang=en&id={file.get_id()}').user('gizmore').exec()
        # test_04 populated this setting on a different in-memory user object.
        # Reload it for this request instead of asserting against that stale value.
        user._vals.pop('avatar_file', None)
        saved = GDO_UserSetting.table().get_by_vals({
            'uset_user': user.get_id(),
            'uset_key': 'avatar_file',
        })
        self.assertEqual(file.get_id(), saved.gdo_val('uset_val'), out)
        self.assertIn(f'file.{file.get_id()}', GDT_Avatar('avatar').for_user(user).render_html())
        self.assertIn('Your avatar has been set.', out)

    def test_06_upload_sets_avatar(self):
        user = web_gizmore()
        boundary = '----PyGDOAvatarUpload'
        with open(Application.file_path('gdo/avatar/img/default.jpeg'), 'rb') as image:
            data = (
                f'--{boundary}\r\n'
                'Content-Disposition: form-data; name="image"; filename="avatar.jpeg"\r\n'
                'Content-Type: image/jpeg\r\n\r\n'
            ).encode() + image.read() + f'\r\n--{boundary}--\r\n'.encode()
        out = web_plug('avatar.upload.html?_lang=en').user('gizmore').post_multipart(data, boundary).exec()
        user._vals.pop('avatar_file', None)
        file_id = GDO_UserSetting.table().get_by_vals({
            'uset_user': user.get_id(),
            'uset_key': 'avatar_file',
        }).gdo_val('uset_val')
        file = GDO_File.table().get_by_id(file_id)
        self.assertTrue(file.is_image(), out)
        self.assertIn(f'file.{file.get_id()}', GDT_Avatar('avatar').for_user(user).render_html())

    async def test_07_gallery_shows_only_non_default_avatars(self):
        custom = await Web.get_server().get_or_create_user('AvatarGalleryCustom')
        default = await Web.get_server().get_or_create_user('AvatarGalleryDefault')
        custom.save_setting('avatar_file', '123')
        default.save_setting('avatar_file', GDT_Avatar.get_default_id())

        out = web_plug('avatar.gallery.html?_lang=en').exec()

        self.assertIn('class="gdt-container avatar-gallery"', out)
        self.assertIn('class="gdt-container gdt-col avatar-gallery-tile"', out)
        self.assertIn('AvatarGalleryCustom', out)
        self.assertIn('file.123', out)
        self.assertNotIn('AvatarGalleryDefault', out)

    def test_08_gallery_sidebar_option(self):
        module = ModuleLoader.instance().get_module('avatar')
        old = module.get_config_val('show_avatar_gallery')
        try:
            # This is a rendering concern. Do not persist a module setting in
            # a test because persisting emits IPC into a different test loop.
            module.config_column('show_avatar_gallery').val('1')
            out = web_plug('core.welcome.html?_lang=en').exec()
            self.assertIn('Avatar Gallery', out)
        finally:
            module.config_column('show_avatar_gallery').val(old)
