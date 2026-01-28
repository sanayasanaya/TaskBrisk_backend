from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Example models: Customize according to your actual models.
from .models import Project, Task, Connection


@api_view(["GET"])
def home_dashboard(request):
    try:
        # Fetch basic dashboard numbers
        total_projects = Project.objects.count()
        completed_projects = Project.objects.filter(status="completed").count()
        remaining_projects = total_projects - completed_projects

        # Connection count example
        total_connections = Connection.objects.count()

        # Task summary for chart
        total_task = Task.objects.count()
        task_completed = Task.objects.filter(status="completed").count()
        task_pending = Task.objects.filter(status="pending").count()
        task_overdue = Task.objects.filter(status="overdue").count()

        # Final response structure exactly matching frontend format
        data = {
            "top": [
                {"title": "Total Project", "value": total_projects, "className": "g1"},
                {"title": "Completed", "value": completed_projects, "className": "g2"},
                {"title": "Remain", "value": remaining_projects, "className": "g3"},
                {"title": "Connection", "value": total_connections, "className": "g4"},
            ],

            "chart": [
                {"name": "Total Task", "value": total_task},
                {"name": "completed", "value": task_completed},
                {"name": "pending", "value": task_pending},
                {"name": "Overdue", "value": task_overdue},
            ],

            "stats": [
                {"label": "total task", "value": total_task},
                {"label": "Completed", "value": task_completed},
                {"label": "Pending", "value": task_pending},
                {"label": "Overdue", "value": task_overdue},
            ],
        }

        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
