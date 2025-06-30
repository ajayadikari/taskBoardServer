from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from board.models import BoardModel
from column.models import ColumnModel
from task.models import TaskModel
from task.serializer import TaskSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_report(request, id):
    # not using id, it is just to follow the api format mentioned in the assignment 
    #using the user obj set by authentication middlewares directly

    user = request.user

    board = BoardModel.objects.filter(user=user).first()

    columns = ColumnModel.objects.filter(board=board)

    todo_tasks = []
    in_progress_tasks = []
    done_tasks = []

    sno = 1
    for column in columns:
        # column_serialized = ColumnSerializer(column).data
        tasks_queryset = TaskModel.objects.filter(column=column)
        for task in tasks_queryset:
            task = TaskSerializer(task).data
            task["sno"] = sno
            if column.status == 't':
                todo_tasks.append(task)
            elif column.status == 'i':
                in_progress_tasks.append(task)
            else:
                done_tasks.append(task)
            sno = sno + 1

    data = {
        "todo": todo_tasks, 
        "in_progress": in_progress_tasks, 
        "done": done_tasks
    }

    print(data)


    html = render_to_string('report.html', context=data) 
    pdf = HTML(string=html).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="board_summary.pdf"'
    return response
