from celery import shared_task
from .service import updateLiveMatches

@shared_task
def matchAppScheduledTask():
    try:
        result = updateLiveMatches()

        if result["success"]:
            return {
                "status": "success",
                "message": f"Matches updated successfully: {result['created']} created, {result['updated']} updated",
                "data": result
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to update matches: {result['error']}"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Task failed with exception: {str(e)}"
        }