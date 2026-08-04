from django.contrib import admin
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "user",
        "city",
        "province",
        "is_default",
    )

    list_filter = (
        "province",
        "is_default",
    )

    search_fields = (
        "full_name",
        "phone",
        "postal_code",
        "user__email",
    )

    