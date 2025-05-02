from django.db import models
from django.utils.translation import gettext_lazy as _


class Goal(models.Model):
    goal_name = models.CharField(_("Цель"), max_length=255)
    approximate_cost = models.PositiveBigIntegerField(_("Приблизительная стоимость"))
    execution_date = models.DateTimeField(_("Срок выполнения"))
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
    )

    def __str__(self):
        return f"Цель - {self.goal_name} до {self.execution_date.strftime("%d.%m.%Y %H:%M")}"

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"
