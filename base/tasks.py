from celery import shared_task


@shared_task
def confirmation():
    print('print to console is sufficient')
    return