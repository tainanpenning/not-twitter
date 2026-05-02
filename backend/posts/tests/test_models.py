import pytest

from posts.models.post import Post
from posts.models.comment import Comment
from posts.models.like import Like
from posts.tests.conftest import UserFactory, PostFactory, CommentFactory, LikeFactory


@pytest.mark.django_db
class TestPostModel:
    """Test suite for Post model."""

    def test_post_creation(self):
        """Test creating a post."""
        author = UserFactory.create()
        post = Post.objects.create(
            author=author,
            content='Test post content',
        )
        assert post.id is not None
        assert post.author == author
        assert post.content == 'Test post content'
        assert post.is_active is True

    def test_post_string_representation(self):
        """Test Post __str__ method."""
        author = UserFactory.create(username='testuser')
        post = PostFactory.create(author=author)
        expected = f'Post by @testuser at {post.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
        assert str(post) == expected

    def test_post_ordering(self):
        """Test posts are ordered by -created_at."""
        author = UserFactory.create()
        post1 = PostFactory.create(author=author, content='Post 1')
        post2 = PostFactory.create(author=author, content='Post 2')
        posts = Post.objects.all()
        assert posts[0].id == post2.id
        assert posts[1].id == post1.id

    def test_post_likes_count(self):
        """Test likes_count property."""
        post = PostFactory.create()
        assert post.likes_count == 0
        LikeFactory.create(post=post)
        LikeFactory.create(post=post, user=UserFactory.create())
        # Refresh to get updated count
        post.refresh_from_db()
        assert post.likes.count() == 2

    def test_post_comments_count(self):
        """Test comments_count property."""
        post = PostFactory.create()
        assert post.comments_count == 0
        CommentFactory.create(post=post)
        CommentFactory.create(post=post, author=UserFactory.create())
        post.refresh_from_db()
        assert post.comments.count() == 2


@pytest.mark.django_db
class TestCommentModel:
    """Test suite for Comment model."""

    def test_comment_creation(self):
        """Test creating a comment."""
        post = PostFactory.create()
        author = UserFactory.create()
        comment = Comment.objects.create(
            post=post,
            author=author,
            content='Test comment',
        )
        assert comment.id is not None
        assert comment.post == post
        assert comment.author == author
        assert comment.is_active is True

    def test_comment_string_representation(self):
        """Test Comment __str__ method."""
        post = PostFactory.create()
        author = UserFactory.create(username='commenter')
        comment = CommentFactory.create(post=post, author=author)
        assert 'commenter' in str(comment)
        assert f'Post ID {post.id}' in str(comment)


@pytest.mark.django_db
class TestLikeModel:
    """Test suite for Like model."""

    def test_like_creation(self):
        """Test creating a like."""
        post = PostFactory.create()
        user = UserFactory.create()
        like = Like.objects.create(post=post, user=user)
        assert like.id is not None
        assert like.post == post
        assert like.user == user

    def test_like_unique_constraint(self):
        """Test unique constraint on (post, user)."""
        post = PostFactory.create()
        user = UserFactory.create()
        LikeFactory.create(post=post, user=user)

        with pytest.raises(Exception):  # IntegrityError
            Like.objects.create(post=post, user=user)

    def test_like_string_representation(self):
        """Test Like __str__ method."""
        post = PostFactory.create()
        user = UserFactory.create(username='liker')
        like = LikeFactory.create(post=post, user=user)
        assert 'liker' in str(like)
        assert f'Post ID {post.id}' in str(like)
