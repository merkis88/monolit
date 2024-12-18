from datetime import timezone, timedelta

from celery import shared_task
from .models import Post

@shared_task
def delete_expired_post():
    expired_posts = Post.objects.filter(created_at__lt=timezone.now() - timedelta(days=('valid_duration')))
    expired_posts.delete()