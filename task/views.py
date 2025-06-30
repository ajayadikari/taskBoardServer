from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from board.models import BoardModel
from column.models import ColumnModel
from .models import TaskModel
from .serializer import TaskSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    try:
        data = request.data

        if not data:
            return Response({
                "success": False, 
                "message": "no data"
            }, status=status.HTTP_400_BAD_REQUEST)
        

        user = request.user

        if not user.is_authenticated:
            return Response({
                "success": False, 
                "message": "please login!"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        board = BoardModel.objects.filter(user=user).first()

        if not board:
            return Response({
                "success": False, 
                "message": "board not found"
            }, status=status.HTTP_404_NOT_FOUND)
        

        todo_column = ColumnModel.objects.filter(board=board, status='t').first()

        if todo_column is None:
            return Response({
                "success": False, 
                "message": "todo column not found!"
            }, status=status.HTTP_404_NOT_FOUND)
        
        task_data = {
            "task": data.get('task', None), 
            "column": todo_column.id
        }
        

        task_serializer = TaskSerializer(data=task_data)

        if not task_serializer.is_valid():
            return Response({
                "success": False, 
                "message": "data is not valid!", 
                "errors": task_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        task_serializer.save()
        return Response({
            "success": True, 
            "message": "task created!", 
            "data": task_serializer.data
        }, status=status.HTTP_200_OK)
    
    except Exception as err:
        print("------------------------")
        print("err -- task app -- create_task()")
        print(err)

        return Response({
            "success": False,
            "message": "something went wrong!", 
            "errors": str(err)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    try: 
        user = request.user

        if not user:
            return Response({
                "success": False, 
                "message": "please login!"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if task_id is None:
            return Response({
                "success": False, 
                "message": "task id is needed!"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        task_ins = TaskModel.objects.filter(id=task_id).first()

        if not task_ins:
            return Response({
                "success": False, 
                "message": "task not found!"
            }, status=status.HTTP_404_NOT_FOUND)

        new_task = request.data.get("task", None)

        if not new_task:
            return Response({
                "success": False,
                "message": "task cannot be empty"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # task_ins.task = new_task
        # task_ins.save()

        updated_task_serializer = TaskSerializer(task_ins, request.data, partial=True)

        if updated_task_serializer.is_valid():
            updated_task_serializer.save()
            return Response({
                "success": True, 
                "message": "task updated!", 
                "data": updated_task_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False, 
                "message": "task is invalid!", 
                "error": str(updated_task_serializer.errors)
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as err:
        print("-------------------")
        print("err - task - update_task()")
        print(str(err))

        return Response({
            "success": False, 
            "message": "unable to update task!", 
            "errors": str(err)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_task_status(request, task_id, new_status):
    try: 
        user = request.user
        
        if not task_id:
            return Response({
                "success": False, 
                "message": "task id is needed!"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        task_ins = TaskModel.objects.filter(id=task_id).first()
        
        if not task_ins:
            return Response({
                "success": False, 
                "message": "task not found!"
            })
        
        if new_status is None:
            return Response({
                "success": False, 
                'message': "status is needed!"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        all_status = ['t', 'i', 'd']

        if new_status not in all_status:
            return Response({
                "success": False, 
                "message": "status can only be t(to do), i(in progress), or d(done)"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        board = BoardModel.objects.filter(user=user).first()

        column = ColumnModel.objects.filter(board=board, status=new_status).first()

        if not column:
            return Response({
                "success": False, 
                "message": "column not found!"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if task_ins.column == column:
            return Response({
                "success": False, 
                "message": "status not changed"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        task_ins.column = column
        update_task_serializer = TaskSerializer(task_ins, data={"column": column.id}, partial=True)

        if update_task_serializer.is_valid():
            update_task_serializer.save()
            return Response({
                "success": True, 
                "message": "task updated!"
            }, status=status.HTTP_200_OK)
        
        else:
            print("----------------------")
            print("err -- task app -- update_task_status()")
            print(update_task_serializer.errors)
            return Response({
                "success": False, 
                "message": "unable to update the task!", 
                "errors": str(update_task_serializer.errors)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
        print("----------------------------------------")
        print("err -- task app -- update_task_status()")
        print(err)
        return Response({
            "status": False, 
            "message": "internal server error", 
            "errors": str(err)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    try:
        user = request.user

        if not task_id: 
            return Response({
                "success": False, 
                "message": "task id is needed!"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        task_ins = TaskModel.objects.filter(id=task_id).first()

        if not task_ins:
            return Response({
                "success": False, 
                "message": "task not found!"
            }, status=status.HTTP_404_NOT_FOUND)
        
        task_ins.delete()

        return Response({
            "success": True, 
            "message": "task deleted!"
        }, status=status.HTTP_200_OK)
    
    except Exception as err:
        print("--------------------------")
        print("err -- task app -- delete_task()")
        print(err)

        return Response({
            "success": False, 
            "message": "internal server error", 
            "errors": str(err)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_tasks(request):
    user = request.user

    board = BoardModel.objects.filter(user=user).first()

    if not board:
        return Response({
            "success": False, 
            "message": "board not found!"
        }, status=status.HTTP_404_NOT_FOUND)
    
    todo_column_ins = ColumnModel.objects.filter(board=board, status="t").first()
    inprogress_column_ins = ColumnModel.objects.filter(board=board, status='i').first()
    done_column_ins = ColumnModel.objects.filter(board=board, status='d').first()

    todo_tasks_queryset = TaskModel.objects.filter(column=todo_column_ins).prefetch_related('column')
    todo_tasks = []
    for task in todo_tasks_queryset:
        todo_tasks.append({
            "id": task.id,
            "task": task.task, 
            "status": task.column.status, 
            "created_at": task.created_at, 
            "updated_at": task.updated_at
        })
    # todo_tasks = TaskSerializer(todo_tasks_queryset, many=True).data

    inprogress_tasks_queryset = TaskModel.objects.filter(column=inprogress_column_ins).prefetch_related('column')
    inprogress_tasks = []
    for task in inprogress_tasks_queryset:
        inprogress_tasks.append({
            "id": task.id,
            "task": task.task, 
            "status": task.column.status, 
            "created_at": task.created_at, 
            "updated_at": task.updated_at
        })

    # inprogress_tasks = TaskSerializer(inprogress_tasks_queryset, many=True).data

    done_tasks_queryset = TaskModel.objects.filter(column=done_column_ins)
    done_tasks = []
    for task in done_tasks_queryset:
        done_tasks.append({
            "id": task.id,
            "task": task.task, 
            "status": task.column.status, 
            "created_at": task.created_at, 
            "updated_at": task.updated_at
        })

    # done_tasks = TaskSerializer(done_tasks_queryset, many=True).data

    return Response({
        "success": True, 
        "message": "tasks fetched!", 
        "tasks": {
            "todo_tasks": todo_tasks, 
            "inprogress_tasks": inprogress_tasks, 
            "done_tasks": done_tasks
        }
    }, status=status.HTTP_200_OK)
    

    
    
    

    
    


    