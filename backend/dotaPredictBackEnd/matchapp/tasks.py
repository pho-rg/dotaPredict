from celery import shared_task

print("📦 matchapp.tasks loaded")

@shared_task
def matchAppScheduledTask():
    print("This task runs every 5 seconds")