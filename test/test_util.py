import unittest
import mock

from lala import util, pluginmanager, config

def f(user, channel, text):
    pass

def f2(arg1, arg2):
    pass

class TestUtil(unittest.TestCase):
    def setUp(self):
        util._PM = mock.Mock(spec=pluginmanager.PluginManager)
        util._BOT = mock.Mock()

    def test_on_join(self):
        util.on_join(f2)
        util._PM.register_join_callback.assert_called_once_with(f2)

    def test_command(self):
        util.command(f)
        util._PM.register_callback.assert_called_once_with("f", f)

    def test_named_command(self):
        c = util.command("command")
        c(f)
        util._PM.register_callback.assert_called_once_with("command", f)

    def test_command_str(self):
        self.assertRaises(TypeError, util.command, object())

    def test_regex(self):
        r = util.regex(".*")
        r(f)
        util._PM.register_regex.assert_called_once_with(".*", f)

    def test_argcheck(self):
        self.assertFalse(util._check_args(f, 2))
        self.assertTrue(util._check_args(f, 3))

        self.assertRaises(TypeError, util.command, f2)
        self.assertRaises(TypeError, util.on_join, f)

        r = util.regex("foobar")
        self.assertRaises(TypeError, r, f2)

    def test_message(self):
        util.msg("user", "message")
        util._BOT.msg.assert_called_once_with("user", "message", True)

        util.msg("user", ["message1", "message2"])
        util._BOT.msg.assert_called_with("user", "message2", True)
        self.assertEqual(len(util._BOT.msg.call_args_list), 3)
        self.assertEqual(util._BOT.msg.call_args_list[1][0][1], "message1")

    def test_empty_message(self):
        util.msg("user", "")
        self.assertFalse(util._BOT.msg.called)
        util.msg("user", ["", ""])
        self.assertFalse(util._BOT.msg.called)

    def test_is_admin(self):
        config._get = mock.Mock(return_value=["superman", "bofh"])

        self.assertTrue(util.is_admin("superman"))
        self.assertFalse(util.is_admin("i'm-no-superman"))
