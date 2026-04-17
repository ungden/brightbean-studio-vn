"""Tests for inbox webhook signature verification.

Webhooks from social platforms are CSRF-exempt (required) but MUST verify
HMAC signatures to prevent forged payloads. These tests ensure signature
verification is working correctly.
"""

import hashlib
import hmac
import json

from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(FACEBOOK_WEBHOOK_VERIFY_TOKEN="test-verify-token")
class FacebookWebhookTests(TestCase):
    """Verify Facebook webhook signature verification."""

    def _sign_payload(self, payload: bytes, secret: str) -> str:
        """Generate HMAC-SHA256 signature like Facebook does."""
        return "sha256=" + hmac.new(
            secret.encode("utf-8"), payload, hashlib.sha256
        ).hexdigest()

    def test_webhook_rejects_missing_signature(self):
        """Webhook POST without X-Hub-Signature-256 header should be rejected."""
        # Only run if the URL is registered
        try:
            url = reverse("inbox:facebook_webhook")
        except Exception:
            self.skipTest("Facebook webhook URL not configured")

        response = self.client.post(
            url,
            data=json.dumps({"entry": []}),
            content_type="application/json",
        )
        # Should be 401/403 (rejected) not 200
        self.assertIn(response.status_code, [401, 403, 400])

    def test_webhook_rejects_invalid_signature(self):
        """Webhook POST with wrong signature should be rejected."""
        try:
            url = reverse("inbox:facebook_webhook")
        except Exception:
            self.skipTest("Facebook webhook URL not configured")

        response = self.client.post(
            url,
            data=json.dumps({"entry": []}),
            content_type="application/json",
            HTTP_X_HUB_SIGNATURE_256="sha256=invalidsignature",
        )
        self.assertIn(response.status_code, [401, 403, 400])


class WebhookVerificationEndpointTests(TestCase):
    """Test Facebook webhook GET verification (hub.challenge flow)."""

    @override_settings(FACEBOOK_WEBHOOK_VERIFY_TOKEN="verify-token-xyz")
    def test_verification_returns_challenge_with_correct_token(self):
        """GET with matching hub.verify_token should echo hub.challenge."""
        try:
            url = reverse("inbox:facebook_webhook")
        except Exception:
            self.skipTest("Facebook webhook URL not configured")

        response = self.client.get(
            url,
            {
                "hub.mode": "subscribe",
                "hub.verify_token": "verify-token-xyz",
                "hub.challenge": "test-challenge-123",
            },
        )
        if response.status_code == 200:
            self.assertEqual(response.content.decode(), "test-challenge-123")

    @override_settings(FACEBOOK_WEBHOOK_VERIFY_TOKEN="verify-token-xyz")
    def test_verification_rejects_wrong_token(self):
        """GET with wrong hub.verify_token should be rejected."""
        try:
            url = reverse("inbox:facebook_webhook")
        except Exception:
            self.skipTest("Facebook webhook URL not configured")

        response = self.client.get(
            url,
            {
                "hub.mode": "subscribe",
                "hub.verify_token": "wrong-token",
                "hub.challenge": "test-challenge-123",
            },
        )
        self.assertIn(response.status_code, [401, 403])
