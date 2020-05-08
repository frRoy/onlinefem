from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FEMConfig(AppConfig):
    name = "onlinefem.fem"
    verbose_name = _("FEM")
