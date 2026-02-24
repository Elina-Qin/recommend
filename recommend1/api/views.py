import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import calculate_optimal_recommendation

# 配置日志（指定日志名称，方便区分其他模块日志）
logger = logging.getLogger('api.calculate')

# ========== 3个独立的全局临时存储变量 ==========
# 分别对应3个上传按钮的最新推荐表单
latest_recommendation_1 = None
latest_recommendation_2 = None
latest_recommendation_3 = None


# ========== 上传接口1：对应第一个上传按钮 ==========
@csrf_exempt
@api_view(['POST'])
def calculate_recommendation_1(request):
    """
    接收前端JSON数据（第一个上传按钮），计算后返回JSON格式推荐表单
    同时将结果存入专属临时存储，覆盖原有数据
    前端请求格式：POST http://localhost:8000/api/calculate/1/
    Headers: Content-Type: application/json
    Body: {total_strategy: [...], single_product_strategy: [...], market_price: [...]}
    """
    logger.info(f"【表单1】收到推荐计算请求 - 客户端IP: {request.META.get('REMOTE_ADDR')}")
    logger.info(f"【表单1】请求体数据: {request.data}")

    #  校验请求体核心字段
    required_keys = ["total_strategy", "single_product_strategy", "market_price"]
    for key in required_keys:
        if key not in request.data:
            error_msg = f"【表单1】缺少必要字段：{key}"
            logger.error(error_msg)
            return Response(
                {"error": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not isinstance(request.data[key], list):
            error_msg = f"【表单1】{key}必须是数组类型（实际类型：{type(request.data[key])}）"
            logger.error(error_msg)
            return Response(
                {"error": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(request.data[key]) == 0:
            warning_msg = f"【表单1】{key}是空数组，可能导致无推荐结果"
            logger.warning(warning_msg)

    try:
        #  调用核心计算函数
        logger.info("【表单1】开始执行推荐计算...")
        recommendation_result = calculate_optimal_recommendation(
            total_strategy_data=request.data["total_strategy"],
            single_product_data=request.data["single_product_strategy"],
            market_price_data=request.data["market_price"]
        )

        #  存入专属临时存储
        global latest_recommendation_1
        latest_recommendation_1 = recommendation_result
        logger.info("【表单1】最新推荐表单已更新到临时存储")

        # 返回结果
        logger.info(f"【表单1】计算完成，生成推荐结果条数: {len(recommendation_result)}")
        return Response({
            "code": 200,
            "message": "【表单1】计算成功",
            "data": recommendation_result,
            "total": len(recommendation_result)
        }, status=status.HTTP_200_OK)

    except Exception as e:
        error_msg = f"【表单1】计算失败：{str(e)}"
        logger.error(error_msg, exc_info=True)
        return Response(
            {"error": error_msg},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== 上传接口2：对应第二个上传按钮 ==========
@csrf_exempt
@api_view(['POST'])
def calculate_recommendation_2(request):
    """
    接收前端JSON数据（第二个上传按钮），计算后返回JSON格式推荐表单
    同时将结果存入专属临时存储，覆盖原有数据
    前端请求格式：POST http://localhost:8000/api/calculate/2/
    """
    logger.info(f"【表单2】收到推荐计算请求 - 客户端IP: {request.META.get('REMOTE_ADDR')}")
    logger.info(f"【表单2】请求体数据: {request.data}")

    # 校验请求体核心字段
    required_keys = ["total_strategy", "single_product_strategy", "market_price"]
    for key in required_keys:
        if key not in request.data:
            error_msg = f"【表单2】缺少必要字段：{key}"
            logger.error(error_msg)
            return Response(
                {"error": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not isinstance(request.data[key], list):
            error_msg = f"【表单2】{key}必须是数组类型（实际类型：{type(request.data[key])}）"
            logger.error(error_msg)
            return Response(
                {"error": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(request.data[key]) == 0:
            warning_msg = f"【表单2】{key}是空数组，可能导致无推荐结果"
            logger.warning(warning_msg)

    try:
        # 调用核心计算函数
        logger.info("【表单2】开始执行推荐计算...")
        recommendation_result = calculate_optimal_recommendation(
            total_strategy_data=request.data["total_strategy"],
            single_product_data=request.data["single_product_strategy"],
            market_price_data=request.data["market_price"]
        )

        # 存入专属临时存储
        global latest_recommendation_2
        latest_recommendation_2 = recommendation_result
        logger.info("【表单2】最新推荐表单已更新到临时存储")

        # 返回结果
        logger.info(f"【表单2】计算完成，生成推荐结果条数: {len(recommendation_result)}")
        return Response({
            "code": 200,
            "message": "【表单2】计算成功",
            "data": recommendation_result,
            "total": len(recommendation_result)
        }, status=status.HTTP_200_OK)

    except Exception as e:
        error_msg = f"【表单2】计算失败：{str(e)}"
        logger.error(error_msg, exc_info=True)
        return Response(
            {"error": error_msg},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== 上传接口3：对应第三个上传按钮 ==========
@csrf_exempt
@api_view(['POST'])
def calculate_recommendation_3(request):
    """
    接收前端JSON数据（第三个上传按钮），计算后返回JSON格式推荐表单
    同时将结果存入专属临时存储，覆盖原有数据
    前端请求格式：POST http://localhost:8000/api/calculate/3/
    """
    logger.info(f"【表单3】收到推荐计算请求 - 客户端IP: {request.META.get('REMOTE_ADDR')}")
    logger.info(f"【表单3】请求体数据: {request.data}")

    #  校验请求体核心字段
    required_keys = ["total_strategy", "single_product_strategy", "market_price"]
    for key in required_keys:
        if key not in request.data:
            error_msg = f"【表单3】缺少必要字段：{key}"
            logger.error(error_msg)
            return Response(
                {"error": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not isinstance(request.data[key], list):
            error_msg = f"【表单3】{key}必须是数组类型（实际类型：{type(request.data[key])}）"
            logger.error(error_msg)
            return Response(
                {"error": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(request.data[key]) == 0:
            warning_msg = f"【表单3】{key}是空数组，可能导致无推荐结果"
            logger.warning(warning_msg)

    try:
        # 调用核心计算函数
        logger.info("【表单3】开始执行推荐计算...")
        recommendation_result = calculate_optimal_recommendation(
            total_strategy_data=request.data["total_strategy"],
            single_product_data=request.data["single_product_strategy"],
            market_price_data=request.data["market_price"]
        )

        # 存入专属临时存储
        global latest_recommendation_3
        latest_recommendation_3 = recommendation_result
        logger.info("【表单3】最新推荐表单已更新到临时存储")

        # 返回结果
        logger.info(f"【表单3】计算完成，生成推荐结果条数: {len(recommendation_result)}")
        return Response({
            "code": 200,
            "message": "【表单3】计算成功",
            "data": recommendation_result,
            "total": len(recommendation_result)
        }, status=status.HTTP_200_OK)

    except Exception as e:
        error_msg = f"【表单3】计算失败：{str(e)}"
        logger.error(error_msg, exc_info=True)
        return Response(
            {"error": error_msg},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== 查看接口1：对应第一个查看按钮 ==========
@csrf_exempt
@api_view(['GET'])
def get_latest_recommendation_1(request):
    """
    供前端第一个查看按钮调用，获取表单1的最新推荐表单
    前端请求格式：GET http://localhost:8000/api/latest-recommendation/1/
    """
    global latest_recommendation_1
    logger.info(f"【表单1】收到获取最新推荐表单请求 - 客户端IP: {request.META.get('REMOTE_ADDR')}")

    if latest_recommendation_1 is None:
        logger.warning("【表单1】临时存储中暂无推荐表单数据")
        return Response({
            "code": 404,
            "message": "【表单1】暂无最新推荐表单数据，请先生成推荐表单",
            "data": [],
            "total": 0
        }, status=status.HTTP_200_OK)

    logger.info(f"【表单1】返回最新推荐表单，数据条数: {len(latest_recommendation_1)}")
    return Response({
        "code": 200,
        "message": "【表单1】获取最新推荐表单成功",
        "data": latest_recommendation_1,
        "total": len(latest_recommendation_1)
    }, status=status.HTTP_200_OK)


# ========== 查看接口2：对应第二个查看按钮 ==========
@csrf_exempt
@api_view(['GET'])
def get_latest_recommendation_2(request):
    """
    供前端第二个查看按钮调用，获取表单2的最新推荐表单
    前端请求格式：GET http://localhost:8000/api/latest-recommendation/2/
    """
    global latest_recommendation_2
    logger.info(f"【表单2】收到获取最新推荐表单请求 - 客户端IP: {request.META.get('REMOTE_ADDR')}")

    if latest_recommendation_2 is None:
        logger.warning("【表单2】临时存储中暂无推荐表单数据")
        return Response({
            "code": 404,
            "message": "【表单2】暂无最新推荐表单数据，请先生成推荐表单",
            "data": [],
            "total": 0
        }, status=status.HTTP_200_OK)

    logger.info(f"【表单2】返回最新推荐表单，数据条数: {len(latest_recommendation_2)}")
    return Response({
        "code": 200,
        "message": "【表单2】获取最新推荐表单成功",
        "data": latest_recommendation_2,
        "total": len(latest_recommendation_2)
    }, status=status.HTTP_200_OK)


# ========== 查看接口3：对应第三个查看按钮 ==========
@csrf_exempt
@api_view(['GET'])
def get_latest_recommendation_3(request):
    """
    供前端第三个查看按钮调用，获取表单3的最新推荐表单
    前端请求格式：GET http://localhost:8000/api/latest-recommendation/3/
    """
    global latest_recommendation_3
    logger.info(f"【表单3】收到获取最新推荐表单请求 - 客户端IP: {request.META.get('REMOTE_ADDR')}")

    if latest_recommendation_3 is None:
        logger.warning("【表单3】临时存储中暂无推荐表单数据")
        return Response({
            "code": 404,
            "message": "【表单3】暂无最新推荐表单数据，请先生成推荐表单",
            "data": [],
            "total": 0
        }, status=status.HTTP_200_OK)

    logger.info(f"【表单3】返回最新推荐表单，数据条数: {len(latest_recommendation_3)}")
    return Response({
        "code": 200,
        "message": "【表单3】获取最新推荐表单成功",
        "data": latest_recommendation_3,
        "total": len(latest_recommendation_3)
    }, status=status.HTTP_200_OK)