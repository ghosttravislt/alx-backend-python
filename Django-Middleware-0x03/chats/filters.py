import django_filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    # Filter by user: messages sent OR received by this user
    user = django_filters.ModelChoiceFilter(
        field_name="sender",
        to_field_name="id",
        queryset=User.objects.all(),
        label="Messages involving this user"
    )

    # Date range filtering
    start_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["user", "start_date", "end_date"]
