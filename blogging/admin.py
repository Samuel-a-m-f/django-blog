from django.contrib import admin
from django import forms
from .models import Post, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


admin.site.register(Category, CategoryAdmin)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()

        return instance


# 👇 Admin setup using the inline form
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('title',)
    filter_horizontal = ('categories',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
