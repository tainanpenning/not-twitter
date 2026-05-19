from django.conf import settings
import hmac
import hashlib
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status


class GithubWebhookViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        github_signature = request.headers.get("X-Hub-Signature-256")

        secret = settings.GITHUB_WEBHOOK_SECRET.encode()

        expected = "sha256=" + hmac.new(secret, request.body, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(expected, github_signature or ""):
            return Response({"error": "Invalid signature"}, status=status.HTTP_403_FORBIDDEN)

        return Response({"ok": True})
