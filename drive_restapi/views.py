from multiprocessing import dummy
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import todayUsersSerializer

# Create your views here.

"""

[ 고객 ]

todayuserView : 현재 들어온 차량
memberView : 고객 멤버십

"""


# import DB models
from .models import today_user
from .models import member
from .serializers import todayUsersSerializer
from .serializers import membersSerializer


# 1. 현재 들어온 차량 뷰
class todayUserView(APIView):
    """
    POST /todayusers -> 현재 들어온 차량 입력
    """
    def post(self, request):
        todayUser_serializer = todayUsersSerializer(data=request.data) #Request의 data를 todayusersSerializer로 변환

        if todayUser_serializer.is_valid(): #유효하면
            todayUser_serializer.save() #todayUsersSerialize 유효성 검사 후 DB에 저장
            return Response(todayUser_serializer.data, status=status.HTTP_201_CREATED) #클라이언트에 JSON response 전달
        else:
            return Response(todayUser_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    """
    GET /todayusers -> 현재 들어온 차량 전부 조회
        /todayusers/{todayuserID} -> 해당 차량 ID만 조회
    """
    def get(self, request, **kwargs):
        if kwargs.get('todayuserID') is None: #api 뒤에 todayuserID가 없으면 전부 조회
            todayUser_queryset = today_user.objects.all()
            todayUser_queryset_serializer = todayUsersSerializer(todayUser_queryset, many=True)
            return Response(todayUser_queryset_serializer.data, status=status.HTTP_200_OK)

        else: #userID가 있으면 해당 아이디만 조회
            todayUser_id = kwargs.get('todayuserID') #url에 있는 id 가져오기
            todayUser_serializer = todayUsersSerializer(today_user.objects.get(todayUserID=todayUser_id)) #id에 해당하는 정보 불러오기
            return Response(todayUser_serializer.data, status=status.HTTP_200_OK)
 
    """
    PUT /todayusers/{todayuserID} -> 모든 컬럼에 데이터 입력해 넘겨줘야 수정 가능함!
    """
    def put(self, request, **kwargs):
        if kwargs.get('todayuserID') is None: #url에 todayuserID 없으면 실패
            return Response("URL에 todayuserID를 추가해야합니다!", status=status.HTTP_400_BAD_REQUEST)
        
        else: #url에 ID 있으면
            todayUser_id = kwargs.get('todayuserID') #todayUser_id 변수에 넣기
            todayUser_object = today_user.objects.get(todayUserID=todayUser_id) #id에 해당하는 객체 인스턴스 가져오기

            update_todayUser_serailizer = todayUsersSerializer(todayUser_object, data=request.data) #새로 요청한 데이터로 직렬화
            if update_todayUser_serailizer.is_valid(): #유효성 검사
                update_todayUser_serailizer.save() #유효하면 DB 저장
                return Response(update_todayUser_serailizer.data, status=status.HTTP_200_OK)
            else: #유효하지 않으면 실패
                return Response("모든 컬럼의 값을 입력해야 합니다!", status=status.HTTP_400_BAD_REQUEST)

    """
    DELETE /todayusers/{todayuserID} -> 현재 들어온 차량 삭제
    """
    def delete(self, request, **kwargs ):
        if kwargs.get('todayuserID') is None: #todayuserID 값이 URL에 없으면
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            todayUser_id = kwargs.get('todayuserID')
            todayUser_object = today_user.objects.get(todayUserID=todayUser_id)
            todayUser_object.delete()
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
            member_queryset = member.objects.all()
            member_queryset_serializer = membersSerializer(member_queryset, many=True)
            return Response(member_queryset_serializer.data, status=status.HTTP_200_OK)

        else: #memberID가 있으면 해당 아이디만 조회
            member_id = kwargs.get('memberID') #url에 있는 id 가져오기
            member_serializer = membersSerializer(member.objects.get(memberID=member_id)) #id에 해당하는 정보 불러오기
            return Response(member_serializer.data, status=status.HTTP_200_OK)
 
 
    """
    PUT /members/{memberID} -> 모든 컬럼에 데이터 입력해 넘겨줘야 수정 가능함!
    """
    def put(self, request, **kwargs):
        if kwargs.get('memberID') is None: #url에 memberID 없으면 실패
            return Response("URL에 memberID를 추가해야합니다!", status=status.HTTP_400_BAD_REQUEST)
        
        else: #url에 ID 있으면
            member_id = kwargs.get('memberID') #member_id 변수에 넣기
            member_object = member.objects.get(memberID=member_id) #id에 해당하는 객체 인스턴스 가져오기

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
            member_object = member.objects.get(memberID=member_id)
            member_object.delete()
            return Response("해당 데이터 삭제", status=200)

class orderView(APIView):
    """
    POST /todayusers -> 현재 들어온 차량 입력
    """


# DB - prods
from .serializers import prodsSerializer
from .models import prod

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
            prod_queryset = prod.objects.all()
            prod_queryset_serializer = prodsSerializer(prod_queryset, many=True)
            return Response(prod_queryset_serializer.data, status=status.HTTP_200_OK)

        else: #prodID가 있으면 해당 아이디만 조회
            prod_id = kwargs.get('prodID') #url에 있는 id 가져오기
            prod_serializer = prodsSerializer(prod.objects.get(prodID=prod_id)) #id에 해당하는 정보 불러오기
            return Response(prod_serializer.data, status=status.HTTP_200_OK)
 
    """
    PUT /prods/{prodID} -> 모든 컬럼에 데이터 입력해 넘겨줘야 수정 가능함!
    """
    def put(self, request, **kwargs):
        if kwargs.get('prodID') is None: #url에 prodID 없으면 실패
            return Response("URL에 prodID를 추가해야합니다!", status=status.HTTP_400_BAD_REQUEST)
        
        else: #url에 ID 있으면
            prod_id = kwargs.get('prodID') #prod_id 변수에 넣기
            prod_object = prod.objects.get(prodID=prod_id) #id에 해당하는 객체 인스턴스 가져오기

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
            prod_object = prod.objects.get(prodID=prod_id)
            prod_object.delete()
            return Response("해당 데이터 삭제", status=200)
