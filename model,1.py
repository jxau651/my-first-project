import pulp

# =========================
# 1. 原料列表
# =========================
ingredients = ["玉米", "豆粕", "麦麸", "石粉","鱼粉"]

# =========================
# 2. 营养参数（每个字典=一种营养）
# =========================

# 粗蛋白 CP (%)
CP = {
    "玉米": 9.5,
    "豆粕": 46.5,
    "麦麸": 17.5,
    "石粉": 0.0,
    "鱼粉":68.0
}

# 消化能 DE (MJ/kg)
DE = {
    "玉米": 14.2,
    "豆粕": 13.0,
    "麦麸": 11.8,
    "石粉": 0.0,
    "鱼粉":10.7
}

# 钙 Ca (%)
Ca = {
    "玉米": 0.02,
    "豆粕": 0.30,
    "麦麸": 0.10,
    "石粉": 38.0,
    "鱼粉": 5.0
}
P = {
    "玉米": 0.25,
    "豆粕": 0.60,
    "麦麸": 0.45,
    "石粉": 0.0,
    "鱼粉": 3.0
}
# =========================
# 3. 营养需求（最低）
# =========================
target_CP = 14.0
target_DE = 13.0
target_Ca = 0.80
target_P =  0.45
# =========================
# 4. 成本（元/kg）
# =========================
cost = {
    "玉米": 2.8,
    "豆粕": 4.5,
    "麦麸": 2.2,
    "石粉": 0.5,
    "鱼粉": 13.2
}

# =========================
# 5. 建立模型
# =========================
model = pulp.LpProblem("Feed_Formulation_MultiNutrient", pulp.LpMinimize)

# =========================
# 6. 决策变量（连续百分比，精度0.01%）
# =========================
y = pulp.LpVariable.dicts(
    "Percent",
    ingredients,
    lowBound=0,
    upBound=100,
    cat="Continuous"  #改成Continuous（连续变量）
)

# =========================
# 7. 目标函数（成本最低）
# =========================
model += pulp.lpSum(cost[i] * y[i] for i in ingredients)

# =========================
# 8. 约束条件
# =========================

# （1）百分比和 = 100
model += pulp.lpSum(y[i] for i in ingredients) == 100

# （2）多营养指标约束（>=）
model += pulp.lpSum(CP[i] * y[i] for i in ingredients) >= target_CP * 100
model += pulp.lpSum(DE[i] * y[i] for i in ingredients) >= target_DE * 100
model += pulp.lpSum(Ca[i] * y[i] for i in ingredients) >= target_Ca * 100
model += pulp.lpSum(P[i] * y[i] for i in ingredients) >= target_P * 100
# =========================
# 9. 求解
# =========================
model.solve()

## =========================
# 10. 输出结果
# =========================
print("最优配方（0.01% 精度）：")
for i in ingredients:
    print(f"{i}: {y[i].value():.2f} %")   # 保留两位小数

# 实际营养水平
actual_CP = sum(CP[i] * y[i].value() for i in ingredients) / 100
actual_DE = sum(DE[i] * y[i].value() for i in ingredients) / 100
actual_Ca = sum(Ca[i] * y[i].value() for i in ingredients) / 100
actual_P = sum(P[i] * y[i].value() for i in ingredients) / 100
total_cost = sum(cost[i] * y[i].value() for i in ingredients) / 100

print("\n实际营养水平：")
print(f"CP = {actual_CP:.2f} %")
print(f"DE = {actual_DE:.2f} MJ/kg")
print(f"Ca = {actual_Ca:.2f} %")
print(f"P = {actual_P:.2f} %")

print(f"\n单位成本 = {total_cost:.3f}")
