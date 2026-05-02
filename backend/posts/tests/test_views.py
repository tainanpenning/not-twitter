import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token

from posts.models.post import Post
from posts.models.comment import Comment
from posts.models.like import Like
from posts.tests.conftest import UserFactory, PostFactory, CommentFactory, LikeFactory


@pytest.mark.django_db
class TestPostViewSet:
    """Test suite for Post viewset."""

    def test_list_posts(self, api_client):
        """Test listing posts."""
        post1 = PostFactory.create()
        post2 = PostFactory.create()

        response = api_client.get('/api/posts/posts/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2

    def test_create_post_authenticated(self, api_client):
        """Test creating a post when authenticated."""
        user = UserFactory.create()
        token = Token.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {
            'content': 'New post',
        }
        response = api_client.post('/api/posts/posts/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1
        assert Post.objects.first().author == user

    def test_create_post_unauthenticated(self, api_client):
        """Test creating a post when unauthenticated."""
        data = {
            'content': 'New post',
        }
        response = api_client.post('/api/posts/posts/', data)
        # IsAuthenticatedOrReadOnly returns 401 when posting as unauthenticated
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

    def test_retrieve_post(self, api_client):
        """Test retrieving a single post."""
        post = PostFactory.create(content='Test content')

        response = api_client.get(f'/api/posts/posts/{post.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['content'] == 'Test content'

    def test_update_post_as_author(self, api_client):
        """Test updating a post as the author."""
        user = UserFactory.create()
        token = Token.objects.create(user=user)
        post = PostFactory.create(author=user, content='Original')

        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'content': 'Updated content'}
        response = api_client.patch(f'/api/posts/posts/{post.id}/', data)

        assert response.status_code == status.HTTP_200_OK
        post.refresh_from_db()
        assert post.content == 'Updated content'

    def test_update_post_not_author(self, api_client):
        """Test updating a post as non-author."""
        author = UserFactory.create()
        other_user = UserFactory.create()
        post = PostFactory.create(author=author)

        token = Token.objects.create(user=other_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'content': 'Hacked'}
        response = api_client.patch(f'/api/posts/posts/{post.id}/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_post_as_author(self, api_client):
        """Test soft-deleting a post as author."""
        user = UserFactory.create()
        token = Token.objects.create(user=user)
        post = PostFactory.create(author=user)

        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = api_client.delete(f'/api/posts/posts/{post.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        post.refresh_from_db()
        assert post.is_active is False

    def test_post_includes_likes_and_comments_count(self, api_client):
        """Test post includes likes and comments count."""
        post = PostFactory.create()
        LikeFactory.create(post=post)
        LikeFactory.create(post=post, user=UserFactory.create())
        CommentFactory.create(post=post)

        response = api_client.get(f'/api/posts/posts/{post.id}/')
        assert response.status_code == status.HTTP_200_OK
        # Check that likes were created
        assert response.data['likes_count'] == 2
        assert response.data['comments_count'] == 1


@pytest.mark.django_db
class TestCommentViewSet:
    """Test suite for Comment viewset."""

    def test_list_comments_by_post(self, api_client):
        """Test listing comments for a post."""
        post = PostFactory.create()
        CommentFactory.create(post=post)
        CommentFactory.create(post=post)

        response = api_client.get(f'/api/posts/comments/?post_id={post.id}')
        assert response.status_code == status.HTTP_200_OK
        # Response might be paginated
        if isinstance(response.data, dict) and 'results' in response.data:
            assert len(response.data['results']) == 2
        else:
            assert len(response.data) == 2

    def test_create_comment_authenticated(self, api_client):
        """Test creating a comment when authenticated."""
        user = UserFactory.create()
        post = PostFactory.create()
        token = Token.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {
            'post': post.id,
            'content': 'Great post!',
        }
        response = api_client.post('/api/posts/comments/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.count() == 1
        assert Comment.objects.first().author == user

    def test_create_comment_unauthenticated(self, api_client):
        """Test creating a comment when unauthenticated."""
        post = PostFactory.create()
        data = {
            'post': post.id,
            'content': 'Nice!',
        }
        response = api_client.post('/api/posts/comments/', data)
        # IsAuthenticated returns 401 when posting as unauthenticated
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

    def test_update_comment_as_author(self, api_client):
        """Test updating a comment as the author."""
        author = UserFactory.create()
        comment = CommentFactory.create(author=author, content='Original')

        token = Token.objects.create(user=author)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'content': 'Updated comment'}
        response = api_client.patch(f'/api/posts/comments/{comment.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        comment.refresh_from_db()
        assert comment.content == 'Updated comment'

    def test_delete_comment_by_post_author(self, api_client):
        """Test deleting a comment as the post author."""
        post_author = UserFactory.create()
        commenter = UserFactory.create()
        post = PostFactory.create(author=post_author)
        comment = CommentFactory.create(post=post, author=commenter)

        token = Token.objects.create(user=post_author)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = api_client.delete(f'/api/posts/comments/{comment.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestLikeViewSet:
    """Test suite for Like viewset."""

    def test_toggle_like_create(self, api_client):
        """Test toggling a like (create)."""
        user = UserFactory.create()
        post = PostFactory.create()
        token = Token.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = api_client.post(f'/api/posts/likes/toggle/{post.id}/')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == True
        assert Like.objects.filter(post=post, user=user).exists()

    def test_toggle_like_delete(self, api_client):
        """Test toggling a like (delete)."""
        user = UserFactory.create()
        post = PostFactory.create()
        LikeFactory.create(post=post, user=user)

        token = Token.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = api_client.post(f'/api/posts/likes/toggle/{post.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'unliked'
        assert not Like.objects.filter(post=post, user=user).exists()

    def test_toggle_like_unauthenticated(self, api_client):
        """Test toggling a like when unauthenticated."""
        post = PostFactory.create()
        response = api_client.post(f'/api/posts/likes/toggle/{post.id}/')
        # IsAuthenticated returns 401 or 403 when posting as unauthenticated
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

    def test_toggle_like_nonexistent_post(self, api_client):
        """Test toggling a like on nonexistent post."""
        user = UserFactory.create()
        token = Token.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = api_client.post('/api/posts/likes/toggle/999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
