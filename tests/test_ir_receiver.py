from __future__ import annotations

import unittest

from automation.orchestrator import ir_receiver


class IRReceiverSecurityTests(unittest.TestCase):
    def test_content_length_rejects_missing_negative_non_numeric_and_oversized(self) -> None:
        for value in (None, "", "-1", "abc", str(ir_receiver.MAX_BODY_BYTES + 1)):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    ir_receiver.parse_content_length(value)

    def test_content_length_accepts_bounded_payload(self) -> None:
        self.assertEqual(ir_receiver.parse_content_length("128"), 128)

    def test_token_check_fails_closed(self) -> None:
        self.assertFalse(ir_receiver.authorized("", "anything"))
        self.assertFalse(ir_receiver.authorized("expected", None))
        self.assertFalse(ir_receiver.authorized("expected", "wrong"))
        self.assertTrue(ir_receiver.authorized("expected", "expected"))


if __name__ == "__main__":
    unittest.main()
