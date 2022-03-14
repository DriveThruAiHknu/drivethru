from multiprocessing import dummy
from django.shortcuts import render

# Create your views here.

# DB - users 모델로 연습
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import usersSerializer
from rest_framework import status
from .models import users


class userView(APIView):
    """
    POST /user
    """
    def post(self, request):
        user_serializer = usersSerializer(data=request.data) #Request의 data를 UserSerializer로 변환

        if user_serializer.is_valid(): #유효하면
            user_serializer.save() #usersSerialize 유효성 검사 후 DB에 저장
            return Response(user_serializer.data, status=status.HTTP_201_CREATED) #클라이언트에 JSON response 전달
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    """
    GET /user -> 전체 조회
    GET /user/{userID} -> 해당 ID만 조회
    """
    def get(self, request, **kwargs):
        if kwargs.get('userID') is None: #api 뒤에 userID가 없으면 전부 조회
            user_queryset = users.objects.all()
            user_queryset_serializer = usersSerializer(user_queryset, many=True)
            return Response(user_queryset_serializer.data, status=status.HTTP_200_OK)

        else: #userID가 있으면 해당 아이디만 조회
            user_id = kwargs.get('userID') #url에 있는 id 가져오기
            user_serializer = usersSerializer(users.objects.get(userID=user_id)) #id에 해당하는 정보 불러오기
            return Response(user_serializer.data, status=status.HTTP_200_OK)
 
    """
    PUT /user/{user_id} -> 모든 컬럼에 데이터 입력해 넘겨줘야 수정 가능함!
    """
    def put(self, request, **kwargs):
        if kwargs.get('userID') is None: #url에 userID 없으면 실패
            return Response("URL에 userID를 추가해야합니다!", status=status.HTTP_400_BAD_REQUEST)
        
        else: #url에 ID 있으면
            user_id = kwargs.get('userID') #user_id 변수에 넣기
            user_object = users.objects.get(userID=user_id) #id에 해당하는 객체 인스턴스 가져오기

            update_user_serailizer = usersSerializer(user_object, data=request.data) #새로 요청한 데이터로 직렬화
            if update_user_serailizer.is_valid(): #유효성 검사
                update_user_serailizer.save() #유효하면 DB 저장
                return Response(update_user_serailizer.data, status=status.HTTP_200_OK)
            else: #유효하지 않으면 실패
                return Response("모든 컬럼의 값을 입력해야 합니다!", status=status.HTTP_400_BAD_REQUEST)


 
    """
    DELETE /user/{user_id}
    """
    def delete(self, request, **kwargs ):
        if kwargs.get('userID') is None: #userID 값이 URL에 없으면
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            user_id = kwargs.get('userID')
            user_object = users.objects.get(userID=user_id)
            user_object.delete()
            return Response("해당 데이터 삭제", status=200)


# 여기서 부터 시작!!
"""

[ 고객 ]

currentuserView : 현재 들어온 차량
memberView : 고객 멤버십

"""


# import DB models
from .models import currentusers
from .models import members
from .serializers import currentusersSerializer
from .serializers import membersSerializer


# 1. 현재 들어온 차량 뷰
class currentuserView(APIView):
    """
    POST /currentusers -> 현재 들어온 차량 입력
    """
    def post(self, request):
        currentuser_serializer = currentusersSerializer(data=request.data) #Request의 data를 currentusersSerializer로 변환

        if currentuser_serializer.is_valid(): #유효하면
            currentuser_serializer.save() #currentusersSerialize 유효성 검사 후 DB에 저장
            return Response(currentuser_serializer.data, status=status.HTTP_201_CREATED) #클라이언트에 JSON response 전달
        else:
            return Response(currentuser_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    """
    GET /currentusers -> 현재 들어온 차량 전부 조회
        /currentusers/{currentuserID} -> 해당 차량 ID만 조회
    """
    def get(self, request, **kwargs):
        if kwargs.get('currentuserID') is None: #api 뒤에 currentuserID가 없으면 전부 조회
            currentuser_queryset = currentusers.objects.all()
            currentuser_queryset_serializer = currentusersSerializer(currentuser_queryset, many=True)
            return Response(currentuser_queryset_serializer.data, status=status.HTTP_200_OK)

        else: #userID가 있으면 해당 아이디만 조회
            currentuser_id = kwargs.get('currentuserID') #url에 있는 id 가져오기
            currentuser_serializer = currentusersSerializer(currentusers.objects.get(currentuserID=currentuser_id)) #id에 해당하는 정보 불러오기
            return Response(currentuser_serializer.data, status=status.HTTP_200_OK)
 
    """
    PUT /currentusers/{currentuserID} -> 모든 컬럼에 데이터 입력해 넘겨줘야 수정 가능함!
    """
    def put(self, request, **kwargs):
        if kwargs.get('currentuserID') is None: #url에 currentuserID 없으면 실패
            return Response("URL에 currentuserID를 추가해야합니다!", status=status.HTTP_400_BAD_REQUEST)
        
        else: #url에 ID 있으면
            currentuser_id = kwargs.get('currentuserID') #currentuser_id 변수에 넣기
            currentuser_object = currentusers.objects.get(currentuserID=currentuser_id) #id에 해당하는 객체 인스턴스 가져오기

            update_currentuser_serailizer = currentusersSerializer(currentuser_object, data=request.data) #새로 요청한 데이터로 직렬화
            if update_currentuser_serailizer.is_valid(): #유효성 검사
                update_currentuser_serailizer.save() #유효하면 DB 저장
                return Response(update_currentuser_serailizer.data, status=status.HTTP_200_OK)
            else: #유효하지 않으면 실패
                return Response("모든 컬럼의 값을 입력해야 합니다!", status=status.HTTP_400_BAD_REQUEST)

    """
    DELETE /currentusers/{currentuserID} -> 현재 들어온 차량 삭제
    """
    def delete(self, request, **kwargs ):
        if kwargs.get('currentuserID') is None: #currentuserID 값이 URL에 없으면
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            currentuser_id = kwargs.get('currentuserID')
            currentuser_object = currentusers.objects.get(currentuserID=currentuser_id)
            currentuser_object.delete()
            return Response("해당 데이터 삭제", status=200)


# 2. 멤버십 고객 뷰
class memberView(APIView):
    """
    POST /members -> 멤버십 고객 추가
    """
    def post(self, request):
        member_serializer = membersSerializer(data=request.data) #Request의 data를 membersSerializer로 변환

        if member_serializer.is_valid(): #유효하면
            member_serializer.save() #membersSerialize 유효성 검사 후 DB에 저장
            return Response(member_serializer.data, status=status.HTTP_201_CREATED) #클라이언트에 JSON response 전달
        else:
            return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    GET /members -> 전체 멤버십 고객 조회
        /members/{memberID} -> 해당 멤버십 ID 고객만 조회
    """
    def get(self, request, **kwargs):
        if kwargs.get('memberID') is None: #api 뒤에 memberID가 없으면 전부 조회
            member_queryset = members.objects.all()
            member_queryset_serializer = membersSerializer(member_queryset, many=True)
            return Response(member_queryset_serializer.data, status=status.HTTP_200_OK)

        else: #memberID가 있으면 해당 아이디만 조회
            member_id = kwargs.get('memberID') #url에 있는 id 가져오기
            member_serializer = membersSerializer(members.objects.get(memberID=member_id)) #id에 해당하는 정보 불러오기
            return Response(member_serializer.data, status=status.HTTP_200_OK)
 
 
    """
    PUT /members/{memberID} -> 모든 컬럼에 데이터 입력해 넘겨줘야 수정 가능함!
    """
    def put(self, request, **kwargs):
        if kwargs.get('memberID') is None: #url에 memberID 없으면 실패
            return Response("URL에 memberID를 추가해야합니다!", status=status.HTTP_400_BAD_REQUEST)
        
        else: #url에 ID 있으면
            member_id = kwargs.get('memberID') #member_id 변수에 넣기
            member_object = members.objects.get(memberID=member_id) #id에 해당하는 객체 인스턴스 가져오기

            update_member_serailizer = membersSerializer(member_object, data=request.data) #새로 요청한 데이터로 직렬화
            if update_member_serailizer.is_valid(): #유효성 검사
                update_member_serailizer.save() #유효하면 DB 저장
                return Response(update_member_serailizer.data, status=status.HTTP_200_OK)
            else: #유효하지 않으면 실패
                return Response("모든 컬럼의 값을 입력해야 합니다!", status=status.HTTP_400_BAD_REQUEST)


    """
    DELETE /members/{memberID} -> 현재 들어온 차량 삭제
    """
    def delete(self, request, **kwargs ):
        if kwargs.get('memberID') is None: #memberID 값이 URL에 없으면
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            member_id = kwargs.get('memberID')
            member_object = members.objects.get(memberID=member_id)
            member_object.delete()
            return Response("해당 데이터 삭제", status=200)

class orderView(APIView):
    """
    POST /currentusers -> 현재 들어온 차량 입력
    """


# DB - prods
from .serializers import prodsSerializer
from .models import prods

# a. 메뉴 목록 출력
class prodView(APIView):
    """
    POST /prods -> 메뉴 입력
    """
    def post(self, request):
        prod_serializer = prodsSerializer(data=request.data) #Request의 data를 prodsSerializer로 변환

        if prod_serializer.is_valid(): #유효하면
            prod_serializer.save() #prodsSerialize 유효성 검사 후 DB에 저장
            return Response(prod_serializer.data, status=status.HTTP_201_CREATED) #클라이언트에 JSON response 전달
        else:
            return Response(prod_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    """
    GET /prods -> 메뉴 전부 조회
        /prods/{prodID} -> 해당 메뉴 ID만 조회
    """
    def get(self, request, **kwargs):
        if kwargs.get('prodID') is None: #api 뒤에 prodID가 없으면 전부 조회
            prod_queryset = prods.objects.all()
            prod_queryset_serializer = prodsSerializer(prod_queryset, many=True)
            return Response(prod_queryset_serializer.data, status=status.HTTP_200_OK)

        else: #prodID가 있으면 해당 아이디만 조회
            prod_id = kwargs.get('prodID') #url에 있는 id 가져오기
            prod_serializer = prodsSerializer(prods.objects.get(prodID=prod_id)) #id에 해당하는 정보 불러오기
            return Response(prod_serializer.data, status=status.HTTP_200_OK)
 
    """
    PUT /prods/{prodID} -> 모든 컬럼에 데이터 입력해 넘겨줘야 수정 가능함!
    """
    def put(self, request, **kwargs):
        if kwargs.get('prodID') is None: #url에 prodID 없으면 실패
            return Response("URL에 prodID를 추가해야합니다!", status=status.HTTP_400_BAD_REQUEST)
        
        else: #url에 ID 있으면
            prod_id = kwargs.get('prodID') #prod_id 변수에 넣기
            prod_object = prods.objects.get(prodID=prod_id) #id에 해당하는 객체 인스턴스 가져오기

            update_prod_serailizer = prodsSerializer(prod_object, data=request.data) #새로 요청한 데이터로 직렬화
            if update_prod_serailizer.is_valid(): #유효성 검사
                update_prod_serailizer.save() #유효하면 DB 저장
                return Response(update_prod_serailizer.data, status=status.HTTP_200_OK)
            else: #유효하지 않으면 실패
                return Response("모든 컬럼의 값을 입력해야 합니다!", status=status.HTTP_400_BAD_REQUEST)

    """
    DELETE /prods/{prodID} -> 현재 들어온 메뉴 삭제
    """
    def delete(self, request, **kwargs ):
        if kwargs.get('prodID') is None: #prodID 값이 URL에 없으면
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            prod_id = kwargs.get('prodID')
            prod_object = prods.objects.get(prodID=prod_id)
            prod_object.delete()
            return Response("해당 데이터 삭제", status=200)
