class PostService:

    @staticmethod
    def soft_delete_post(post):
        post.is_active = False
        post.save(update_fields=['is_active'])
        post.comments.update(is_active=False)
        post.likes.all().delete()
