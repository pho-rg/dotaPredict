from celery import shared_task
from .service import updateLiveMatches, updateWinnerMatches

@shared_task
def updateMatchesScheduledTask():
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

@shared_task
def updateWinnerScheduledTask():
    try:
        result = updateWinnerMatches()

        if result["success"]:
            return {
                "status": "success",
                "message": f"Winner matches updated successfully: {result['updated']} updated, {result['not_found']} set as unknown, {result['total']} total processed",
                "data": result
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to update winner matches: {result['error']}"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Winner matches task failed with exception: {str(e)}"
        }