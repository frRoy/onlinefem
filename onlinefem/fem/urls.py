from django.urls import path

from onlinefem.fem.views import (
    dolfin_view,
)

app_name = "fem"
urlpatterns = [
    path("", view=dolfin_view, name="dolfin"),
]
