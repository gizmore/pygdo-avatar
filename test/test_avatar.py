import os
import unittest

from gdo.avatar.GDO_Avatar import GDO_Avatar
from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.base.Util import module_enabled
from gdo.core.GDO_Session import GDO_Session
from gdotest.TestUtil import web_plug, reinstall_module, web_gizmore, install_module


class AvatarTest(unittest.TestCase):

    def setUp(self):
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        Application.init_cli()
        Application.set_session(GDO_Session.for_user(web_gizmore()))
        loader = ModuleLoader.instance()
        loader.load_modules_db()
        loader.init_modules(load_vals=True)
        install_module('avatar')
        return self

    def test_00_install(self):
        reinstall_module('avatar')
        self.assertTrue(module_enabled('avatar'), 'cannot install avatar')

    def test_01_upload_form(self):
        out = web_plug('avatar.upload.html').exec()
        self.assertIn('image', out, 'Avatar upload file is not rendered.')

    def test_02_render(self):
        avatar = GDO_Avatar.for_user(web_gizmore())
        out = avatar.render_html()
        self.assertIn('avatar', out, 'cannot render avatar.')


    def test_03_upload_text(self):
        data = b'-----------------------------283687824923932629242982017982\r\nContent-Disposition: form-data; name=\"test\"\r\n\r\ngjgjgj\r\n-----------------------------283687824923932629242982017982\r\nContent-Disposition: form-data; name=\"image\"; filename=\"AnschreibenAndrena.txt\"\r\nContent-Type: text/plain\r\n\r\nHallo,\n\nIch bewerbe mich f\\xc3\\xbcr eine Anstellung als Programmierer,\n\nIch heisse Christian, bin 43 Jahre alt, und komme aus Peine, Niedersachsen.\n\nIch spreche einige Programmiersprachen fliessend, darunter PHP, Java, Jacascript, Python, Ruby und C.\n\nIm Design bin ich nicht der beste, kann aber Anforderungen in CSS umsetzen.\n\nIch bin der Kopf und Programmierer hinter www.wechall.net und kenne mich auch in Datenbanken etwas aus.\n\nMeherer GB CSV streame ich zum Fr\\xc3\\xbchst\\xc3\\xbcck ^^\n\nIch hoffe ich habe interesse geweckt.\n\nViele Gr\\xc3\\xbc\\xc3\\x9fe\nChristian Busch\ngizmore@wechall.net\n\n\r\n-----------------------------283687824923932629242982017982\r\nContent-Disposition: form-data; name=\"csrf\"\r\n\r\n243e71619862\r\n-----------------------------283687824923932629242982017982\r\nContent-Disposition: form-data; name=\"submit\"\r\n\r\nSubmit\r\n-----------------------------283687824923932629242982017982--\r\n'
        out = web_plug('avatar.upload.html').post_multipart(data, '---------------------------283687824923932629242982017982').exec()
        self.assertIn('Only images are allowed', out, 'Can upload text file to avatars.')
