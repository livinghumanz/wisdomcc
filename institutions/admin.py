from django.contrib import admin

from .models import Brand, BrandSection, Branch, Program, TeamMember


class ProgramInline(admin.TabularInline):
    model = Program
    extra = 0
    fields = ['name', 'age_range', 'admissions_open', 'order']
    ordering = ['order']
    show_change_link = True


class BrandSectionInline(admin.TabularInline):
    model = BrandSection
    extra = 0
    fields = ['title', 'nav_label', 'key', 'layout', 'is_published', 'order']
    ordering = ['order']
    show_change_link = True


class BranchInline(admin.TabularInline):
    model = Branch
    extra = 0
    fields = ['name', 'phone', 'is_active', 'order']
    ordering = ['order']
    show_change_link = True


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'slug', 'is_active', 'order']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('short_name',)}
    inlines = [ProgramInline, BrandSectionInline, BranchInline]
    fieldsets = [
        ('Identity', {
            'fields': ['name', 'short_name', 'slug', 'descriptor', 'tagline', 'logo'],
            'description': 'The brand name is a field so it can be changed without a code release.',
        }),
        ('Home page copy', {'fields': ['welcome_heading', 'intro', 'about']}),
        ('Vision & mission', {'fields': ['vision', 'mission']}),
        ('Admissions', {'fields': ['admissions_note']}),
        ('Visibility', {'fields': ['is_active', 'order']}),
    ]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'brand', 'is_published', 'order']
    list_filter = ['brand', 'is_published']
    list_editable = ['order', 'is_published']
    search_fields = ['name', 'role', 'bio']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'age_range', 'admissions_open', 'order']
    list_filter = ['brand', 'admissions_open']
    list_editable = ['order', 'admissions_open']
    search_fields = ['name', 'intro', 'focus_areas']


@admin.register(BrandSection)
class BrandSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'nav_label', 'brand', 'key', 'layout', 'is_published', 'order']
    list_filter = ['brand', 'layout', 'is_published']
    list_editable = ['order', 'is_published']
    search_fields = ['title', 'bullets']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'phone', 'email', 'is_active', 'order']
    list_filter = ['brand', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'address', 'phone']
    fieldsets = [
        (None, {'fields': ['brand', 'name', 'address', 'phone', 'email', 'is_active', 'order']}),
        ('Links', {'fields': ['maps_url', 'facebook_url', 'instagram_url', 'youtube_url',
                              'whatsapp_number', 'whatsapp_channel_url']}),
        ('Payment', {'fields': ['payment_qr']}),
    ]
