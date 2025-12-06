import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# =========================
# USER CUSTOMIZADO
# =========================
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        USER = "USER", "Usuário"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # CASE SENSITIVE → importante: evitar .lower()
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.USER,
    )

    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    def is_admin(self) -> bool:
        return self.role == self.Roles.ADMIN

    def delete(self, using=None, keep_parents=False):
        """
        Soft delete + anonimização.
        Mantém registro pro histórico dos logs.
        """
        self.is_active = False
        self.is_deleted = True

        # anonimizar para proteger dados pessoais
        self.email = f"deleted+{self.pk}@example.com"
        self.username = f"deleted_{self.pk}"
        self.first_name = ""
        self.last_name = ""

        self.save(update_fields=[
            "is_active", "is_deleted", "email",
            "username", "first_name", "last_name", "updated_at"
        ])

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")

# =========================
# ENUMS DE ORDEM DE SERVIÇO
# =========================
class ServiceOrderType(models.TextChoices):
    ADMINISTRATIVE = "administrative", _("Administrativa")
    INSTALLATION = "installation", _("Instalação")
    PREVENTIVE_MAINTENANCE = "preventive_maintenance", _("Manutenção Preventiva")
    CORRECTIVE_MAINTENANCE = "corrective_maintenance", _("Manutenção Corretiva")
    PREDICTIVE_MAINTENANCE = "predictive_maintenance", _("Manutenção Preditiva")
    INSPECTION = "inspection", _("Vistoria")
    TECHNICAL_ASSISTANCE = "technical_assistance", _("Assistência Técnica")
    WORK_SAFETY = "work_safety", _("Segurança do Trabalho")
    BUDGET = "budget", _("Orçamento")
    EVENTS = "events", _("Eventos")


class ServiceOrderStatus(models.TextChoices):
    OPEN = "open", _("Aberta")
    IN_PROGRESS = "in_progress", _("Em andamento")
    COMPLETED = "completed", _("Concluída")
    CANCELLED = "cancelled", _("Cancelada")


class ServiceProviderType(models.TextChoices):
    TECHNICAL = "technical", _("Técnico")
    SPECIALIZED = "specialized", _("Especializado")
    CONSULTING = "consulting", _("Consultivo")
    ADMINISTRATIVE = "administrative_provider", _("Administrativo")
    LOGISTICS = "logistics", _("Logístico")
    OPERATIONAL = "operational", _("Operacional")
    TECHNOLOGICAL = "technological", _("Tecnológico")
    COMMERCIAL = "commercial", _("Comercial")
    MAINTENANCE = "maintenance_provider", _("Manutenção")
    SECURITY = "security", _("Segurança")
    EDUCATIONAL = "educational", _("Educacional")
    COMMUNICATION = "communication", _("Comunicação")
    OTHER = "other", _("Outros Serviços")


class ServiceOrderPriority(models.TextChoices):
    CRITICAL = "critical", _("Crítica")
    HIGH = "high", _("Alta")
    MEDIUM = "medium", _("Média")
    LOW = "low", _("Baixa")


# =========================
# ORDEM DE SERVIÇO
# =========================
class OrderService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # para rastreio e integração
    protocol = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text=_("Protocolo único da O.S."),
    )
    so_number = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_("Número da O.S."),
    )

    type = models.CharField(
        max_length=50,
        choices=ServiceOrderType.choices,
        default=ServiceOrderType.CORRECTIVE_MAINTENANCE,
        verbose_name=_("Tipo de Serviço"),
    )
    status = models.CharField(
        max_length=50,
        choices=ServiceOrderStatus.choices,
        default=ServiceOrderStatus.OPEN,
        verbose_name=_("Status"),
    )
    provider = models.CharField(
        max_length=50,
        choices=ServiceProviderType.choices,
        default=ServiceProviderType.TECHNICAL,
        verbose_name=_("Prestador"),
    )
    priority = models.CharField(
        max_length=50,
        choices=ServiceOrderPriority.choices,
        default=ServiceOrderPriority.MEDIUM,
        verbose_name=_("Prioridade"),
    )

    recipient_name = models.CharField(
        max_length=255,
        verbose_name=_("Nome do Recebedor/Cliente"),
    )
    cpf = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        verbose_name=_("CPF"),
    )

    description = models.TextField(verbose_name=_("Descrição"))

    # Datas
    open_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Data de abertura"),
    )
    sla_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Data/hora de SLA"),
    )

    # Auditoria básica
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders_created",
        verbose_name=_("Criado por"),
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="orders_updated",
        verbose_name=_("Atualizado por"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    is_deleted = models.BooleanField(default=False, verbose_name=_("Deletado (lógico)"))

    class Meta:
        verbose_name = _("Ordem de Serviço")
        verbose_name_plural = _("Ordens de Serviço")
        ordering = ["-created_at"]

    def __str__(self):
        return f"O.S. {self.so_number} ({self.get_status_display()})"


# =========================
# LOG / AUDITORIA DE O.S.
# =========================
class OrderServiceLog(models.Model):
    class ChangeType(models.TextChoices):
        CREATED = "CREATED", _("Criado")
        UPDATED = "UPDATED", _("Atualizado")
        DELETED = "DELETED", _("Deletado")

    order_service = models.ForeignKey(
        OrderService,
        related_name="logs",
        on_delete=models.CASCADE,
        verbose_name=_("Ordem de Serviço"),
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Alterado por"),
    )
    changed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Data da alteração"),
    )
    change_type = models.CharField(
        max_length=10,
        choices=ChangeType.choices,
        verbose_name=_("Tipo de alteração"),
    )
    old_values = models.JSONField(null=True, blank=True, verbose_name=_("Valores antigos"))
    new_values = models.JSONField(null=True, blank=True, verbose_name=_("Novos valores"))

    class Meta:
        ordering = ["-changed_at"]
        verbose_name = _("Log de O.S.")
        verbose_name_plural = _("Logs de O.S.")
