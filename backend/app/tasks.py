from app.celery_app import celery_app


@celery_app.task(name="jobs.noop")
def noop() -> dict:
    return {"ok": True}

