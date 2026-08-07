from django.utils import timezone
from healthplanapp.models import HealthProfile


def calculate_age(date_of_birth):
    if not date_of_birth:
        return None
    today = timezone.localdate()
    age = today.year -date_of_birth.year
    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        age -= 1

    return age


def calculate_bmi(weight, height):
    if not weight or not height:
        return None
    w = float(weight)
    h = float(height)

    if w <0 or h<0:
        return None
    height_m = h / 100
    bmi = w / (height_m * height_m)
    return round(bmi, 2)



def build_health_context(user):
    profile = HealthProfile.objects.prefetch_related("health_issues__parent").get(user=user)

    health_issues = []

    for issue in profile.health_issues.all():
        health_issues.append({
            "code": issue.code,
            "name": issue.name,
            "kind": issue.kind,
            "parent_code": issue.parent.code if issue.parent else None,
            "parent_name": issue.parent.name if issue.parent else None,
        })

    return {
        "age": calculate_age(profile.date_of_birth),
        "gender": profile.gender,
        "weight": float(profile.weight) if profile.weight else None,
        "height": float(profile.height) if profile.height else None,
        "bmi": calculate_bmi(profile.weight, profile.height),
        "activity_level": profile.activity_level,
        "goal": profile.goal,
        "target_weight": float(profile.target_weight) if profile.target_weight else None,
        "health_issues": health_issues,
        "other_health_issue": profile.other_health_issue if profile.other_health_issue else None,
    }