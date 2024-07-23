import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Board(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    slug = models.SlugField(max_length=40, blank=True)
    description = models.TextField(max_length=500, blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="created_boards")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _('Board')
        verbose_name_plural = _("Boards")
        get_latest_by = 'id'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class List(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    slug = models.SlugField(max_length=40, blank=True)
    description = models.TextField(max_length=500, blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='created_lists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _('List')
        verbose_name_plural = _("Lists")
        get_latest_by = 'id'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Card(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    slug = models.SlugField(max_length=40, blank=True)
    description = models.TextField(max_length=500, blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='created_cards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _('Card')
        verbose_name_plural = _("Cards")
        get_latest_by = 'id'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class BoardMember(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='boards')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('Board Member')
        verbose_name_plural = _("Board Members")
        get_latest_by = 'id'
        unique_together = ('board', 'user',)

    def __str__(self):
        return f"{self.board.name} - {self.user.first_name} {self.user.sur_name}"


class ListMember(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='lists')
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('List Member')
        verbose_name_plural = _("List Members")
        get_latest_by = 'id'
        unique_together = ('list', 'user',)

    def __str__(self):
        return f"{self.list.name} - {self.user.first_name} {self.user.sur_name}"


class CardMember(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='cards')
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('Card Member')
        verbose_name_plural = _("Card Members")
        get_latest_by = 'id'
        unique_together = ('card', 'user',)

    def __str__(self):
        return f"{self.card.name} - {self.user.first_name} {self.user.sur_name}"


class CardAttachment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/', verbose_name=_('Attachment'))
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('Card Attachment')
        verbose_name_plural = _("Card Attachments")
        get_latest_by = 'id'

    def __str__(self):
        return f"{self.card.name} - {self.file.name}"


class CardComment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=500, verbose_name=_('Comment'))
    is_active = models.BooleanField(default=True)
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('Card Comment')
        verbose_name_plural = _("Card Comments")
        get_latest_by = 'id'

    def __str__(self):
        return f"{self.card.name} - {self.user.first_name} {self.user.sur_name}"
