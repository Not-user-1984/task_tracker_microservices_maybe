# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import UserAssignment
# from .kafka_producer import kafka_producer


# @receiver(post_save, sender=UserAssignment)
# def send_user_assignment_to_kafka(sender, instance, **kwargs):
#     print("Сигнал сработал!")
#     """
#     Отправляет данные о назначении пользователя в Kafka после сохранения.
#     """
#     data = {
#         "user": instance.user.oid,
#         "project_id": instance.project.id,
#         "team_id": instance.team.id if instance.team else None,
#     }

#     kafka_producer.send_message(
#         topic="user-assignments",
#         key=str(instance.user.id),
#         value=str(data),
#     )
#     print(f"Отправлено сообщение в Kafka: {data}")