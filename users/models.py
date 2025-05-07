from django.db import models
from django.core.files.base import ContentFile
from PIL import Image
from django.contrib.auth.models import User
import io


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='profile_images/default_profile.png', upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # Resize the uploaded image
    def save(self, *args, **kwargs):
        # Check if the instance already exists (to avoid creating duplicates)
        if self.pk:
            try:
                old_profile = Profile.objects.get(pk=self.pk)
                if old_profile.profile_image != self.profile_image:
                    self.resize_image()
            except Profile.DoesNotExist:
                pass
        else:
            self.resize_image()

        super().save(*args, **kwargs)  # Save the instance only once

    def resize_image(self):
        if self.profile_image and hasattr(self.profile_image, 'file'):
            img = Image.open(self.profile_image.file)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)

                # Save the resized image in memory
                img_io = io.BytesIO()
                img.save(img_io, format=img.format)

                # Save resized image
                self.profile_image.save(self.profile_image.name, ContentFile(img_io.getvalue()), save=False)
