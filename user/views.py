from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import UserSerializer
from rest_framework import status
from board.models import BoardModel
from column.models import ColumnModel
from .models import UserModel
from rest_framework import status

# authentication is pending, dont forget to implement

@api_view(['POST'])
def register(request):
    user_data = request.data

    if user_data.get("username", None) is None:
        return Response({
            "success": False, 
            "message": "username cannot be empty"
        }, status=status.HTTP_400_BAD_REQUEST) 

    user = UserModel.objects.filter(username=user_data["username"]).first()

    if user:
        return Response({
            "success": False, 
            "message": "username already exists"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serialized_data = UserSerializer(data=user_data)

    if serialized_data.is_valid():
        try: 
            user = UserModel.objects.create_user(user_data)
            # create a board, 3 columns instances for every new registered users
            board = BoardModel.objects.create(user=user)
            todo_column_instance = ColumnModel.objects.create(board=board, status='t')
            inProgress_column_instance = ColumnModel.objects.create(board=board, status='i')
            done_column_instance = ColumnModel.objects.create(board=board, status='d')

            return Response({
                "success": True ,
                "message": "user creation successful", 
                "data": str(user)
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("-----------------")
            print("err - user model - register view")
            print(e)

            return Response({
                "success": False, 
                "message": "user creation failed", 
                "errors": str(e)
            }, status=status.HTTP_501_NOT_IMPLEMENTED)
    else:
        return Response({
            "success": False, 
            "message": "data is invalid!", 
            "errors": str(serialized_data.errors)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

