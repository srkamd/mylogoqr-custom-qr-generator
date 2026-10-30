import base64
import re
import unittest

from api.index import escape_vcard_value, escape_wifi_value, handle_mcp_request


class TestMcpPrivacyAndValidation(unittest.TestCase):
    def call_tool(self, name, arguments):
        return handle_mcp_request({
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        })

    def test_wifi_secrets_are_not_repeated_in_result_text(self):
        ssid = "PRIVATE_SSID_SENTINEL"
        password = "PRIVATE_PASSWORD_SENTINEL"
        result = self.call_tool("create_wifi_qr", {"ssid": ssid, "password": password})
        content = result["result"]["content"][0]["text"]
        self.assertNotIn(ssid, content)
        self.assertNotIn(password, content)
        self.assertIn("Wi-Fi QR code", content)
        image_data = re.search(r"data:image/png;base64,([^)]+)", content).group(1)
        self.assertTrue(base64.b64decode(image_data).startswith(b"\x89PNG\r\n\x1a\n"))

    def test_contact_and_whatsapp_details_are_not_repeated(self):
        contact = self.call_tool("create_vcard_qr", {
            "firstName": "PRIVATE_FIRST_SENTINEL",
            "lastName": "PRIVATE_LAST_SENTINEL",
            "phone": "PRIVATE_PHONE_SENTINEL",
        })["result"]["content"][0]["text"]
        self.assertNotIn("PRIVATE_FIRST_SENTINEL", contact)
        self.assertNotIn("PRIVATE_PHONE_SENTINEL", contact)

        whatsapp = self.call_tool("create_whatsapp_qr", {
            "phone": "15550123456",
            "message": "PRIVATE_MESSAGE_SENTINEL",
        })["result"]["content"][0]["text"]
        self.assertNotIn("PRIVATE_MESSAGE_SENTINEL", whatsapp)
        self.assertNotIn("15550123456", whatsapp)

    def test_wifi_and_vcard_fields_escape_delimiters(self):
        self.assertEqual(escape_wifi_value('Office;Net:2'), r'Office\;Net\:2')
        self.assertEqual(escape_vcard_value('A;B,C\nD'), r'A\;B\,C\nD')

    def test_invalid_or_oversized_inputs_return_actionable_errors(self):
        empty = self.call_tool("create_qr_code", {"text": ""})
        self.assertIn("error", empty)
        bad_color = self.call_tool("create_qr_code", {"text": "https://example.com", "darkColor": "red"})
        self.assertIn("error", bad_color)
        too_long = self.call_tool("create_qr_code", {"text": "x" * 2001})
        self.assertIn("error", too_long)

    def test_required_fields_and_unknown_tool_return_errors(self):
        self.assertIn("error", self.call_tool("create_wifi_qr", {"ssid": ""}))
        self.assertIn("error", self.call_tool("create_whatsapp_qr", {"phone": "not-a-number"}))
        self.assertIn("error", self.call_tool("create_vcard_qr", {"firstName": "", "phone": ""}))
        self.assertIn("error", self.call_tool("missing_tool", {}))

    def test_valid_url_qr_result_does_not_echo_payload(self):
        result = self.call_tool("create_qr_code", {"text": "https://private.example/sentinel"})
        content = result["result"]["content"][0]["text"]
        self.assertNotIn("private.example", content)
        self.assertIn("QR code", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)




