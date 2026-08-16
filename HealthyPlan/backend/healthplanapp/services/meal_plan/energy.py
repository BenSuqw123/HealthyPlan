from decimal import Decimal, ROUND_HALF_UP

from django.utils import timezone

from healthplanapp.models import HealthProfile
from healthplanapp.services.meal_plan.strategies import get_meal_plan_strategy


ACTIVITY_FACTORS = {HealthProfile.ActivityLevel.SEDENTARY: Decimal("1.2"), HealthProfile.ActivityLevel.LIGHT: Decimal("1.375"), HealthProfile.ActivityLevel.MODERATE: Decimal("1.55"), HealthProfile.ActivityLevel.ACTIVE: Decimal("1.725"), HealthProfile.ActivityLevel.VERY_ACTIVE: Decimal("1.9")}


def calculate_age(date_of_birth):
    today = timezone.localdate()
    age = today.year - date_of_birth.year
    birthday_not_reached = (today.month, today.day) < (date_of_birth.month, date_of_birth.day)

    return age - int(birthday_not_reached)


def calculate_bmr(health_profile):
    age = calculate_age(health_profile.date_of_birth)

    if age < 18:
        raise ValueError("Công thức hiện tại chỉ áp dụng cho người từ 18 tuổi.")

    bmr = Decimal("10") * health_profile.weight + Decimal("6.25") * health_profile.height - Decimal("5") * Decimal(age)

    if health_profile.gender == HealthProfile.Gender.MALE:
        bmr += Decimal("5")
    elif health_profile.gender == HealthProfile.Gender.FEMALE:
        bmr -= Decimal("161")
    else:
        raise ValueError("Giới tính trong hồ sơ sức khỏe không hợp lệ.")

    return bmr.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_tdee(health_profile):
    bmr = calculate_bmr(health_profile)
    activity_factor = ACTIVITY_FACTORS.get(health_profile.activity_level)

    if activity_factor is None:
        raise ValueError("Mức độ vận động không hợp lệ.")

    tdee = bmr * activity_factor

    return tdee.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_energy_target(health_profile):
    age = calculate_age(health_profile.date_of_birth)
    bmr = calculate_bmr(health_profile)
    tdee = calculate_tdee(health_profile)
    strategy = get_meal_plan_strategy(health_profile.goal)
    target_calories = strategy.calculate_target_calories(tdee)

    return {"age": age, "bmr": bmr, "tdee": tdee, "goal": health_profile.goal, "target_calories": target_calories}