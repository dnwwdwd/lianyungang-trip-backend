from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import (LoginSerializer, \
                             RegisterSerializer, UserSerializer, UserUpdateSerializer,
                             ScenicSerializer, StrategySerializer, ReserveVOSerializer, StrategyVOSerializer,
                             EvaluationSerializer, StrategyStarVOSerializer, ScenicStarSerializer,
                             ScenicStarVOSerializer, StrategyStarSerializer)
from evaluation.models import Evaluation
from reserve.models import Reserve
from scenic.models import Scenic
from strategy.models import Strategy
from strategy_star.models import StrategyStar
from scenic_star.models import ScenicStar
from user.models import User


def custom_login(request, user):
    request.session['userId'] = user.id
    request.session['username'] = user.username
    request.session['nickname'] = user.nickname
    request.session['role'] = user.role
    request.session.set_expiry(3600)


@api_view(['POST'])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = User.objects.get(username=username, password=password)
        if user is not None:
            custom_login(request, user)  # 登录用户并创建 session
            serializer = UserSerializer(user)
            return Response({"code": 0, "data": serializer.data, "message": ""})
        else:
            return Response({"code": 40000, "data": "", "message": "用户不存在"})
    return Response({"code": 40000, "data": "", "message": ""})


@api_view(['POST'])
def user_register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        checkPassword = serializer.validated_data['checkPassword']
        nickname = serializer.validated_data['nickname']
        if password != checkPassword:
            return Response({'code': 40000, "data": [], "message": ""})
        if User.objects.filter(username=username).exists():
            return Response({'code': 40000, "data": [], "message": "账号已存在"})
        user = User(
            username=username,
            password=password,
            nickname=nickname,
            avatarUrl='https://hejiajun-img-bucket.oss-cn-wuhan-lr.aliyuncs.com/hm/56e55a4c-90d4-49c7-99e0-54a600f7afdd.jpg',
            role='user',
        )
        user.save()
        serializer = UserSerializer(user)
        return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def user_logout(request):
    logout(request)
    request.session.flush()
    return Response({"code": 0, "message": "登出成功"})


@api_view(['GET'])
def user_current(request):
    if request.method == 'GET':
        userId = request.session.get('userId')
        if userId is None:
            return Response({"code": 40100, "data": "", "message": "用户未登录"})
        user = User.objects.get(id=userId)
        return Response({"code": 0, "data": UserSerializer(user).data, "message": ""})

@api_view(['POST'])
def user_update(request):
    if request.method == 'POST':
        user_id = request.data.get('id')
        if user_id is None:
            return Response({"code": 40001, "data": "", "message": "缺少用户 ID"})
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"code": 40400, "data": "", "message": "用户未找到"})
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"code": 0, "data": serializer.data, "message": "更新成功"})
        return Response({"code": 40000, "data": serializer.errors, "message": "更新失败"})


@api_view(['GET'])
def user_list(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.get(id=userId)
    if user.role == 'user':
        return Response({"code": 0, "data": "", "message": "无权限"})
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def user_delete(request, id):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.get(id=userId)
    if user.role == 'user':
        return Response({"code": 0, "data": "", "message": "无权限"})
    if userId == id:
        return Response({"code": 40000, "data": "", "message": "自己不能删除自己"})
    user = User.objects.get(id=id)
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    user.delete()
    return Response({"code": 0, "data": True, "message": ""})


@api_view(['POST'])
def user_add(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.get(id=userId)
    if user.role == 'user':
        return Response({"code": 0, "data": "", "message": "无权限"})
    username = request.data.get('username')
    users = User.objects.filter(username=username)
    if not users.exists():
        password = request.data.get('password')
        nickname = request.data.get('nickname')
        avatarUrl = request.data.get('avatarUrl')
        email = request.data.get('email')
        phone = request.data.get('phone')
        address = request.data.get('address')
        user = User(username=username, password=password, nickname=nickname, avatarUrl=avatarUrl, email=email,
                    role='user',
                    phone=phone, address=address)
        user.save()
        return Response({"code": 0, "data": True, "message": ""})


@api_view(['GET'])
def scenic_list(request):
    searchText = request.GET.get('searchText')
    if searchText is None:
        scenics = Scenic.objects.all()
        serializer = ScenicSerializer(scenics, many=True)
        return Response({"code": 0, "data": serializer.data, "message": ""})
    scenics = Scenic.objects.filter(name__icontains=searchText)
    serializer = ScenicSerializer(scenics, many=True)
    return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['GET'])
def scenic_detail(request, id):
    scenic = Scenic.objects.filter(id=id).first()
    if scenic is None:
        return Response({"code": 40000, "data": "", "message": "景区不存在"})
    serializer = ScenicSerializer(scenic)
    return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def scenic_add(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    if user.role == 'user':
        return Response({"code": 40000, "data": "", "message": "无权限"})
    serializer = ScenicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"code": 0, "data": True, "message": ""})


@api_view(['POST'])
def scenic_update(request, id):
    try:
        scenic = Scenic.objects.get(id=id)
    except Scenic.DoesNotExist:
        return Response({"code": 40000, "data": "", "message": ""})
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    if user.role == 'user':
        return Response({"code": 40000, "data": "", "message": "无权限"})
    serializer = ScenicSerializer(scenic, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"code": 0, "data": True, "message": ""})
    return Response({"code": 40000, "data": "", "message": serializer.errors})


@api_view(['POST'])
def scenic_delete(request, id):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    if user.role == 'user':
        return Response({"code": 40000, "data": "", "message": "无权限"})
    scenics = Scenic.objects.filter(id=id)
    if scenics.exists():
        scenics.delete()
        return Response({"code": 0, "data": True, "message": ""})
    return Response({"code": 40000, "data": "", "message": "景区不存在"})


@api_view(['POST'])
def reserve_add(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    scenicId = request.data.get('scenicId')
    reserveTime = request.data.get('reserveTime')
    lastReserve = Reserve.objects.filter(scenicId=scenicId, userId=userId).order_by('-reserveTime').first()
    if lastReserve is not None:
        lastReserveTime = lastReserve.reserveTime
        reserve = Reserve(userId=userId, scenicId=scenicId, reserveTime=reserveTime, lastReserveTime=lastReserveTime)
        reserve.save()
        return Response({"code": 0, "data": True, "message": ""})
    reserve = Reserve(userId=userId, scenicId=scenicId, reserveTime=reserveTime)
    reserve.save()
    return Response({"code": 0, "data": True, "message": ""})


@api_view(['GET'])
def reserve_get_my(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    update_reserve_status()
    reserves = Reserve.objects.filter(userId=userId)
    return Response({"code": 0, "data": ReserveVOSerializer(reserves, many=True).data, "message": ""})


@api_view(['GET'])
def reserve_get_all(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    if user.role == 'user':
        return Response({"code": 40000, "data": "", "message": "无权限"})
    reserves = Reserve.objects.all()
    return Response({"code": 0, "data": ReserveVOSerializer(reserves, many=True).data, "message": ""})


@api_view(['GET'])
def reserve_detail(request, id):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    reserve = Reserve.objects.filter(id=id).first()
    return Response({"code": 0, "data": ReserveVOSerializer(reserve).data, "message": ""})


@api_view(['POST'])
def strategy_add(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    strategy = Strategy(userId=userId, **request.data)
    strategy.save()
    return Response({"code": 0, "data": True, "message": ""})


@api_view(['POST'])
def strategy_delete(request, id):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user.role == 'user':
        return Response({"code": 40000, "data": "", "message": "无权限"})
    strategies = Strategy.objects.filter(id=id)
    strategies.delete()
    return Response({"code": 0, "data": True, "message": ""})


@api_view(['GET'])
def strategy_list(request):
    strategies = Strategy.objects.all()
    page = request.GET.get('page')
    pageSize = request.GET.get('pageSize')
    if page is None or pageSize is None:
        return Response({"code": 0, "data": StrategyVOSerializer(strategies, many=True).data, "message": ""})
    strategies = paginate(strategies, page, pageSize)
    strategyList = Strategy.objects.all()
    return Response({"code": 0, "data": StrategyVOSerializer(strategies, many=True).data, "message": "", "total": strategyList.count()})


@api_view(['POST'])
def strategy_update(request, id):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    if user.role == 'user':
        return Response({"code": 40000, "data": "", "message": "无权限"})
    strategy = Strategy.objects.filter(id=id).first()
    serializer = StrategySerializer(strategy, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"code": 0, "data": True, "message": ""})
    return Response({"code": 40000, "data": "", "message": serializer.errors})


@api_view(['GET'])
def strategy_detail(request, id):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    strategy = Strategy.objects.filter(id=id).first()
    return Response({"code": 0, "data": StrategyVOSerializer(strategy).data, "message": ""})


@api_view(['POST'])
def evaluation_add(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    evaluation = Evaluation(userId=userId, **request.data)
    evaluation.save()
    reserve = Reserve.objects.filter(id=request.data.get('reserveId')).first()
    reserve.evaluationId = evaluation.id
    reserve.status = 3
    reserve.save()
    scenic = Scenic.objects.filter(id=reserve.scenicId).first()
    scenic.score = (scenic.score + request.data.get('score')) / 2
    return Response({"code": 0, "data": True, "message": ""})

@api_view(['GET'])
def evaluation_detail(request, id):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    if user.role == 'user':
        return Response({"code": 40000, "data": "", "message": "无权限"})
    evaluation = Evaluation.objects.filter(id=id).first()
    return Response({"code": 0, "data": EvaluationSerializer(evaluation).data, "message": ""})

@api_view(['GET'])
def get_strategy_star(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    strategyStars = StrategyStar.objects.filter(userId=userId)
    page = request.GET.get('page')
    pageSize = request.GET.get('pageSize')
    if page is None or pageSize is None:
        return Response({"code": 0, "data": StrategyStarVOSerializer(strategyStars, many=True).data, "message": ""})
    strategyStars = paginate(strategyStars, page, pageSize)
    return Response({"code": 0, "data": StrategyStarVOSerializer(strategyStars, many=True).data, "message": ""})

@api_view(['GET'])
def get_scenic_star(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    scenicStars = ScenicStar.objects.filter(userId=userId)
    return Response({"code": 0, "data": ScenicStarVOSerializer(scenicStars, many=True).data, "message": ""})

@api_view(['POST'])
def strategy_star_add(request):
    strategyId = request.data.get('strategyId')
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    strategyStar = StrategyStar(strategyId=strategyId, userId=userId)
    strategyStar.save()
    return Response({"code": 0, "data": True, "message": ""})

@api_view(['POST'])
def strategy_star_delete(request):
    strategyId = request.data.get('strategyId')
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    strategyStar = StrategyStar.objects.filter(strategyId=strategyId, userId=userId)
    strategyStar.delete()
    return Response({"code": 0, "data": True, "message": ""})

@api_view(['POST'])
def scenic_star_add(request):
    scenicId = request.data.get('scenicId')
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    scenicStar = ScenicStar(scenicId=scenicId, userId=userId)
    scenicStar.save()
    return Response({"code": 0, "data": True, "message": ""})

@api_view(['POST'])
def scenic_star_delete(request):
    scenicId = request.data.get('scenicId')
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    scenicStar = ScenicStar.objects.filter(scenicId=scenicId, userId=userId)
    scenicStar.delete()
    return Response({"code": 0, "data": True, "message": ""})

@api_view(['GET'])
def strategy_starred(request):
    strategyId = request.GET.get('strategyId')
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    strategyStar = StrategyStar.objects.filter(userId=userId, strategyId=strategyId)
    if strategyStar.exists():
        return Response({"code": 0, "data": True, "message": ""})
    return Response({"code": 0, "data": False, "message": ""})

@api_view(['GET'])
def scenic_starred(request):
    scenicId = request.GET.get('scenicId')
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.filter(id=userId).first()
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    scenicStar = ScenicStar.objects.filter(userId=userId, scenicId=scenicId)
    if scenicStar.exists():
        return Response({"code": 0, "data": True, "message": ""})
    return Response({"code": 0, "data": False, "message": ""})

def update_reserve_status():
    # 获取当前时间
    now = timezone.now()
    # 查询所有 Reserve 数据
    reserves = Reserve.objects.all()
    for reserve in reserves:
        # 判断 reserveTime 是否大于当前时间
        if reserve.reserveTime < now:
            reserve.status = 1
            reserve.save()  # 保存更新
        # 如果 evaluationId 为空且 status 为 1，将 status 改为 2
        if reserve.evaluationId is None and reserve.status == 1:
            reserve.status = 2
            reserve.save()  # 保存更新
        # 如果 evaluationId 不为空且 status 为 2，将 status 改为 3
        if reserve.evaluationId is not None and reserve.status == 2:
            reserve.status = 3
            reserve.save()  # 保存更新


def paginate(queryset, page, page_size):
    paginator = Paginator(queryset, page_size)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，则返回第一页
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，则返回最后一页
        paginated_queryset = paginator.page(paginator.num_pages)
    return paginated_queryset
