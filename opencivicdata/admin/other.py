from django.contrib import admin
from .. import models
from .base import ModelAdmin, ReadOnlyTabularInline, ContactDetailInline, LinkInline


@admin.register(models.Division)
class DivisionAdmin(ModelAdmin):
    list_display = ('name', 'id')
    search_fields = list_display
    fields = readonly_fields = ('id', 'name', 'redirect', 'country')
    ordering = ('id',)


class LegislativeSessionInline(ReadOnlyTabularInline):
    model = models.LegislativeSession
    readonly_fields = ('identifier', 'name', 'classification', 'start_date', 'end_date')
    ordering = ('-identifier',)


@admin.register(models.Jurisdiction)
class JurisdictionAdmin(ModelAdmin):
    list_display = ('name', 'id')
    readonly_fields = fields = ('id', 'name', 'division', 'classification',
                                'feature_flags', 'extras', 'url')
    ordering = ('id',)
    inlines = [LegislativeSessionInline]


class PostContactDetailInline(ContactDetailInline):
    model = models.PostContactDetail


class PostLinkInline(LinkInline):
    model = models.PostLink


@admin.register(models.Post)
class PostAdmin(ModelAdmin):
    readonly_fields = ('id', 'label', 'organization', 'division', 'extras', 'role')
    fields = readonly_fields + (('start_date', 'end_date'), )
    list_display = ('label', 'organization', 'division')
    list_filter = ('organization__jurisdiction__name',)
    ordering = ('organization__name',)
    inlines = [
        PostContactDetailInline,
        PostLinkInline,
    ]
    search_fields = ('organization__name', 'label')
