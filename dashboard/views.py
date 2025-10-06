from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dashboard.models import InterviewDetails, PresentationPractice, CommunicationPractice, CustomQuestionSet, CustomQuestion, UserProfile

# ---------------- Dashboard Pages ---------------- #

@login_required
def dashboard_view(request):
    return render(request, "dashboard/dashboard.html")

@login_required
def my_sessions(request):
    return render(request, "dashboard/my_sessions.html")

@login_required
def uploaded_items(request):
    return render(request, "dashboard/uploaded_items.html")

@login_required
def analytics(request):
    return render(request, "dashboard/analytics.html")

@login_required
def category_view(request):
    return render(request, "dashboard/category.html")

# ---------------- Interview Requirements ---------------- #
@login_required
def interview_requirements_view(request):
    try:
        interview = InterviewDetails.objects.get(user=request.user)
    except InterviewDetails.DoesNotExist:
        interview = None

    if request.method == "POST":
        if interview:
            interview_instance = interview
        else:
            interview_instance = InterviewDetails(user=request.user)

        interview_instance.full_name = request.POST.get("full_name")
        interview_instance.email = request.POST.get("email")
        interview_instance.phone = request.POST.get("phone")
        interview_instance.education = request.POST.get("education")
        interview_instance.branch = request.POST.get("branch")
        interview_instance.skills = request.POST.get("skills")
        interview_instance.experience = request.POST.get("experience")
        interview_instance.about_you = request.POST.get("about_you")
        interview_instance.role = request.POST.get("role")
        interview_instance.domain = request.POST.get("domain")
        interview_instance.difficulty = request.POST.get("difficulty")
        interview_instance.mode = request.POST.get("mode")
        interview_instance.time_per_question = int(request.POST.get("time_per_question", 60))
        interview_instance.num_questions = int(request.POST.get("num_questions", 5))
        interview_instance.custom_keywords = request.POST.get("custom_keywords")

        if request.FILES.get("resume_file"):
            interview_instance.resume_file = request.FILES["resume_file"]

        interview_instance.save()
        return redirect("dashboard:ai_page")

    return render(request, "dashboard/interview_requirements.html")


# ---------------- Presentation Requirements ---------------- #
@login_required
def presentation_requirements_view(request):
    if request.method == "POST":
        PresentationPractice.objects.create(
            user=request.user,
            topic_name=request.POST.get("topic_name"),
            description=request.POST.get("description"),
            audience_type=request.POST.get("audience_type"),
            ppt_file=request.FILES.get("ppt_file"),
            time_per_question=request.POST.get("time_per_question", 60),
            num_questions=request.POST.get("num_questions", 5),
            custom_keywords=request.POST.get("custom_keywords")
        )
        return redirect("dashboard:dashboard")

    return render(request, "dashboard/presentation_requirements.html")


# ---------------- Communication Requirements ---------------- #
@login_required
def communication_requirements_view(request):
    if request.method == "POST":
        CommunicationPractice.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            age=request.POST.get("age"),
            email=request.POST.get("email"),
            language=request.POST.get("language"),
            language_proficiency=request.POST.get("language_proficiency"),
            mode=request.POST.get("mode"),
            reason=request.POST.get("reason"),
            custom_reason=request.POST.get("custom_reason"),
            time_per_round=int(request.POST.get("time_per_round", 60)),
            num_rounds=int(request.POST.get("num_rounds", 3)),
        )
        return redirect("dashboard:dashboard")

    return render(request, "dashboard/communication_requirements.html")


# ---------------- Custom Questions ---------------- #
@login_required
def question_requirements_view(request):
    if request.method == "POST":
        question_set = CustomQuestionSet.objects.create(
            user=request.user,
            topic_name=request.POST.get("topic_name"),
            short_description=request.POST.get("short_description"),
            num_questions=int(request.POST.get("num_questions", 5)),
            time_per_question=int(request.POST.get("time_per_question", 60))
        )

        questions = []
        for key, value in request.POST.items():
            if key.startswith("question_") and value.strip():
                questions.append(CustomQuestion(question_set=question_set, question_text=value.strip()))
        CustomQuestion.objects.bulk_create(questions)

        return redirect("dashboard:dashboard")

    return render(request, "dashboard/question_requirements.html")


# ---------------- Profile ---------------- #
@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "dashboard/profile.html", {"profile": profile, "user": request.user})

@login_required
def profile_edit_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        profile.gender = request.POST.get("gender")
        profile.dob = request.POST.get("dob")
        profile.bio = request.POST.get("bio")

        if "profile_picture" in request.FILES:
            profile.profile_picture = request.FILES["profile_picture"]

        profile.save()
        return redirect("dashboard:profile")

    return render(request, "dashboard/profile_edit.html", {
        "profile": profile,
        "user": request.user
    })

#=======================================================================================================================



def ai_page_view(request):
    return render(request, 'dashboard/ai_page.html')