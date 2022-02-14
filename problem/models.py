from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from problem.tasks import notify_user

class Created(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        'account.User', on_delete=models.DO_NOTHING,
        related_name='problems'
    )

    def __str__(self):
        return f"{self.title} -> Author: {self.author.email}"


class Image(Created):
    image = models.ImageField(upload_to='images')
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE,
        related_name='images'
    )


class Reply(Created):
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE,
        related_name='replies'
    )
    author = models.ForeignKey(
        'account.User', on_delete=models.DO_NOTHING,
        related_name='replies'
    )
    body = models.TextField()
    image = models.ImageField(upload_to='reply_images')

    def __str__(self):
        return f"Reply to : {self.problem.title}"

    class Meta:
        ordering = ('-created', )


@receiver(post_save, sender=Problem)
def notify_about_creation(sender, instance, created, **kwargs):
    if created:
        # print(instance.author.email)
        # print('-----------------------------------------------------------------------')
        notify_user.delay(instance.author.email)

# @receiver(pre_save, sender=Problem)
# def a(sender, instance, **kwargs):

