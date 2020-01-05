import asyncio
import unittest

from bot.cogs.sync.syncers import Syncer
from bot import constants
from tests import helpers


class TestSyncer(Syncer):
    """Syncer subclass with mocks for abstract methods for testing purposes."""

    name = "test"
    _get_diff = helpers.AsyncMock()
    _sync = helpers.AsyncMock()


class SyncerBaseTests(unittest.TestCase):
    """Tests for the syncer base class."""

    def setUp(self):
        self.bot = helpers.MockBot()
        self.syncer = TestSyncer(self.bot)

    def test_instantiation_fails_without_abstract_methods(self):
        """The class must have abstract methods implemented."""
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class"):
            Syncer(self.bot)

    def test_send_prompt_edits_message_content(self):
        """The contents of the given message should be edited to display the prompt."""
        msg = helpers.MockMessage()
        asyncio.run(self.syncer._send_prompt(msg))

        msg.edit.assert_called_once()
        self.assertIn("content", msg.edit.call_args[1])

    def test_send_prompt_gets_channel_from_cache(self):
        """The dev-core channel should be retrieved from cache if an extant message isn't given."""
        mock_channel = helpers.MockTextChannel()
        mock_channel.send.return_value = helpers.MockMessage()
        self.bot.get_channel.return_value = mock_channel

        asyncio.run(self.syncer._send_prompt())

        self.bot.get_channel.assert_called_once_with(constants.Channels.devcore)
