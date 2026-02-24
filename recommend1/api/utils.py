import logging

logger = logging.getLogger(__name__)

def calculate_optimal_recommendation(total_strategy_data, single_product_data, market_price_data):
    recommendations = []

    # 1. 数据预处理
    total_strategy_dict = {
        item["gear"]: {
            "s1": item.get("s1", 0), "s2": item.get("s2", 0), "s3": item.get("s3", 0),
            "s4": item.get("s4", 0), "s5": item.get("s5", 0), "s6": item.get("s6", 0),
            "s7": item.get("s7", 0), "s8": item.get("s8", 0), "s9": item.get("s9", 0),
            "s10": item.get("s10", 0), "s11": item.get("s11", 0), "s12": item.get("s12", 0),
            "not_participate": item.get("not_participate", 0)
        }
        for item in total_strategy_data
        if 1 <= item.get("gear", 0) <= 30
    }
    logger.info(f"总量策略覆盖 {len(total_strategy_dict)}/30 个档位")

    single_product_dict = {
        (item["卷烟编码"], item["价位段"]): {
            str(gear): item.get(str(gear), 0) for gear in range(1, 31)
        }
        for item in single_product_data
        if item.get("卷烟编码") and item.get("价位段") is not None
    }
    logger.info(f"单品策略覆盖 {len(single_product_dict)} 个（编码, 价位段）组合")

    market_price_dict = {
        item["卷烟编码"]: {
            "cigarette_name": item.get("卷烟名称", "未知名称"),
            "profit": round(item.get("市场零售价", 0) - item.get("批发价", 0), 2)
        }
        for item in market_price_data
        if item.get("卷烟编码")
    }

    logger.info(f"市场价格覆盖 {len(market_price_dict)} 个卷烟编码")

    price_segment_mapping = [
        (1, "S1", "s1"), (2, "S2", "s2"), (3, "S3", "s3"),
        (4, "S4", "s4"), (5, "S5", "s5"), (6, "S6", "s6"),
        (7, "S7", "s7"), (8, "S8", "s8"), (9, "S9", "s9"),
        (10, "S10", "s10"), (11, "S11", "s11"), (12, "S12", "s12"),
        ("不参与", "不参与", "not_participate")
    ]

    # 价位段显示格式映射
    price_segment_display_mapping = {
        "S1": "价位段1-2",
        "S2": "S2",
        "S3": "价位段3",
        "S4": "价位段4-5",
        "S5": "S5",
        "S6": "价位段6",
        "S7": "价位段7",
        "S8": "价位段8",
        "S9": "价位段9",
        "S10": "价位段10",
        "S11": "价位段11",
        "S12": "价位段12",
        "不参与": "不参与"
    }
    for gear in range(1, 31):
        current_total = total_strategy_dict.get(gear)
        if not current_total:
            logger.warning(f"档位 {gear} 无总量策略数据，跳过")
            continue

        for segment_value, segment_name, segment_field in price_segment_mapping:
            max_segment_qty = current_total.get(segment_field, 0)
            if max_segment_qty <= 0:
                logger.debug(f"档位 {gear} - 价位段 {segment_name} 最大数量为0，跳过")
                continue

            available_products = []
            for (code, seg), day_qtys in single_product_dict.items():
                if seg != segment_value:
                    continue
                max_product_qty = day_qtys.get(str(gear), 0)
                if max_product_qty <= 0:
                    continue
                price_info = market_price_dict.get(code)
                if not price_info:
                    logger.debug(f"卷烟 {code} 无市场价格数据，跳过")
                    continue

                # 存储产品原始最大可提供数量（不提前限制，后续统一计算）
                available_products.append({
                    "code": code,
                    "name": price_info["cigarette_name"],
                    "profit": price_info["profit"],
                    "max_product_qty": max_product_qty
                })

            if available_products:
                #按利润降序排序（允许负利润，优先级：利润高→低）
                sorted_products = sorted(available_products, key=lambda x: x["profit"], reverse=True)
                remaining_qty = max_segment_qty  # 需满足的总量策略数量
                selected_products = []

                # 累计选取产品，直到满足总量要求或无产品可选
                for product in sorted_products:
                    if remaining_qty <= 0:
                        break
                    # 本次选取数量 = 产品最大可提供量 和 剩余需求量 的较小值
                    take_qty = min(product["max_product_qty"], remaining_qty)
                    if take_qty > 0:
                        selected_products.append({
                            "code": product["code"],
                            "name": product["name"],
                            "profit": product["profit"],
                            "qty": take_qty
                        })
                        remaining_qty -= take_qty

                # 生成推荐记录
                display_segment = price_segment_display_mapping.get(segment_name, segment_name)
                for p in selected_products:
                    recommendations.append({
                        "档位": gear,
                        "价位段": display_segment,
                        "卷烟编码": p["code"],
                        "卷烟名称": p["name"],
                        "单支利润": p["profit"],
                        "推荐数量": p["qty"]
                    })

                # 日志警告：可用产品不足以满足总量要求（仅记录，不阻断）
                if remaining_qty > 0:
                    logger.warning(
                        f"档位 {gear} - 价位段 {segment_name}（显示：{display_segment}）"
                        f" 可用产品不足，仅满足 {max_segment_qty - remaining_qty}/{max_segment_qty} 数量要求"
                    )
            else:
                # 无可用产品时记录警告
                display_segment = price_segment_display_mapping.get(segment_name, segment_name)
                logger.warning(
                    f"档位 {gear} - 价位段 {segment_name}（显示：{display_segment}）"
                    f" 无可用产品，无法满足 {max_segment_qty} 数量要求"
                )

    logger.info(f"最终生成 {len(recommendations)} 条推荐")
    return recommendations