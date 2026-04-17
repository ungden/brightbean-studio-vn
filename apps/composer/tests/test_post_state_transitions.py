"""Tests for PlatformPost state machine transitions.

Covers the VALID_TRANSITIONS enforcement to ensure status transitions follow
the documented workflow: draft → pending_review → approved → scheduled → publishing → published.
"""

from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import User
from apps.composer.models import PlatformPost, Post
from apps.members.models import OrgMembership, WorkspaceMembership
from apps.organizations.models import Organization
from apps.social_accounts.models import SocialAccount
from apps.workspaces.models import Workspace


class PlatformPostStateTransitionTests(TestCase):
    """Verify PlatformPost state transitions are properly enforced."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="author@example.com",
            password="testpass123",
            tos_accepted_at=timezone.now(),
        )
        self.org = Organization.objects.create(name="Test Org")
        self.workspace = Workspace.objects.create(
            organization=self.org, name="Test Workspace"
        )
        OrgMembership.objects.create(
            user=self.user,
            organization=self.org,
            org_role=OrgMembership.OrgRole.OWNER,
        )
        WorkspaceMembership.objects.create(
            user=self.user,
            workspace=self.workspace,
            workspace_role=WorkspaceMembership.WorkspaceRole.OWNER,
        )
        self.social_account = SocialAccount.objects.create(
            workspace=self.workspace,
            platform="facebook",
            account_platform_id="fb_123",
            account_name="Test Page",
        )
        self.post = Post.objects.create(
            workspace=self.workspace,
            author=self.user,
            caption="Test caption",
        )
        self.platform_post = PlatformPost.objects.create(
            post=self.post,
            social_account=self.social_account,
            status="draft",
        )

    def test_draft_can_transition_to_pending_review(self):
        """draft → pending_review should be allowed."""
        self.assertTrue(self.platform_post.can_transition_to("pending_review"))

    def test_draft_cannot_transition_to_published(self):
        """Cannot skip directly from draft to published."""
        self.assertFalse(self.platform_post.can_transition_to("published"))

    def test_approved_can_transition_to_scheduled(self):
        """approved → scheduled is a valid path."""
        self.platform_post.status = "approved"
        self.platform_post.save()
        self.assertTrue(self.platform_post.can_transition_to("scheduled"))

    def test_published_is_terminal_state(self):
        """Once published, cannot transition to any other status."""
        self.platform_post.status = "published"
        self.platform_post.save()
        self.assertFalse(self.platform_post.can_transition_to("draft"))
        self.assertFalse(self.platform_post.can_transition_to("scheduled"))

    def test_changes_requested_can_return_to_draft(self):
        """changes_requested → draft allows author to resume editing."""
        self.platform_post.status = "changes_requested"
        self.platform_post.save()
        self.assertTrue(self.platform_post.can_transition_to("draft"))


class WorkspaceIsolationTests(TestCase):
    """Verify workspace-scoped queries don't leak between workspaces."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpass123",
            tos_accepted_at=timezone.now(),
        )
        self.org = Organization.objects.create(name="Test Org")

        # Create two workspaces
        self.workspace_a = Workspace.objects.create(
            organization=self.org, name="Workspace A"
        )
        self.workspace_b = Workspace.objects.create(
            organization=self.org, name="Workspace B"
        )

        # User is member of workspace A only
        OrgMembership.objects.create(
            user=self.user,
            organization=self.org,
            org_role=OrgMembership.OrgRole.MEMBER,
        )
        WorkspaceMembership.objects.create(
            user=self.user,
            workspace=self.workspace_a,
            workspace_role=WorkspaceMembership.WorkspaceRole.EDITOR,
        )

        # Create posts in each workspace
        Post.objects.create(
            workspace=self.workspace_a, author=self.user, caption="Post in A"
        )
        Post.objects.create(
            workspace=self.workspace_b, author=self.user, caption="Post in B"
        )

    def test_workspace_scoped_manager_filters_by_workspace(self):
        """WorkspaceScopedManager should return only posts for the given workspace."""
        posts_a = Post.objects.for_workspace(self.workspace_a.id)
        posts_b = Post.objects.for_workspace(self.workspace_b.id)

        self.assertEqual(posts_a.count(), 1)
        self.assertEqual(posts_b.count(), 1)
        self.assertEqual(posts_a.first().caption, "Post in A")
        self.assertEqual(posts_b.first().caption, "Post in B")
