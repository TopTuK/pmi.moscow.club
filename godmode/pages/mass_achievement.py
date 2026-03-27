from django import forms
from django.template.loader import render_to_string
from django_q.tasks import async_task

from notifications.email.achievements import send_new_achievement_email
from notifications.telegram.achievements import notify_user_new_achievement
from users.models.achievements import Achievement, UserAchievement
from users.models.user import User
from common.regexp import USER_URL_RE


class GodmodeMassAchievementForm(forms.Form):
    achievement = forms.ModelChoiceField(
        label="Ачивка",
        queryset=Achievement.objects.filter(is_visible=True),
        empty_label="---",
    )

    recipients = forms.CharField(
        label="Получатели (ники или ссылки на профили с новой строки)",
        required=True,
        max_length=10000,
        widget=forms.Textarea(
            attrs={
                "maxlength": 50000,
                "placeholder": "https://pmi.moscow/user/vas3k/\nhttps://pmi.moscow/user/moderator/\nhttps://pmi.moscow/user/petrovich/",
            }
        ),
    )


def extract_slugs(recipients):
    result = []
    for line in recipients.strip().split():
        matched_url = USER_URL_RE.match(line)
        result.append(matched_url.group(1) if matched_url else line)
    return result


def mass_achievement(request, admin_page):
    if request.method == "POST":
        form = GodmodeMassAchievementForm(request.POST, request.FILES)
        if form.is_valid():
            slugs = extract_slugs(form.cleaned_data["recipients"])
            users = User.objects.filter(slug__in=slugs)
            for user in users:
                user_achievement, is_created = UserAchievement.objects.get_or_create(
                    user=user,
                    achievement=form.cleaned_data["achievement"],
                )
                if is_created:
                    async_task(send_new_achievement_email, user_achievement)
                    async_task(notify_user_new_achievement, user_achievement)

            some_user_not_found = len(slugs) != users.count()
            return render_to_string("godmode/pages/message.html", {
                "title": f"🏆 Ачивка '{form.cleaned_data['achievement'].name}' выдана {users.count()} юзерам",
                "message": "Вот эти юзеры не найдены в Клубе, возможно ошибка в нике: " + ", ".join(
                    list(set(slugs) - set([u.slug for u in users]))
                ) if some_user_not_found else "Все юзеры получили ачивки!"
            }, request=request)
    else:
        form = GodmodeMassAchievementForm()

    return render_to_string("godmode/pages/simple_form.html", {
        "form": form
    }, request=request)
