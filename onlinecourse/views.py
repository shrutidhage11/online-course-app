
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Course, Question, Choice, Submission, Enrollment


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        enrollment = get_object_or_404(
            Enrollment,
            user=request.user,
            course=course
        )

        submission = Submission.objects.create(
            enrollment=enrollment
        )

        selected_choices = []

        for key in request.POST:
            if key.startswith("choice"):
                for choice_id in request.POST.getlist(key):
                    if choice_id.isdigit():
                        choice = get_object_or_404(
                            Choice,
                            pk=int(choice_id)
                        )
                        selected_choices.append(choice)

        submission.choices.set(selected_choices)

        return redirect(
            "onlinecourse:show_exam_result",
            course_id=course.id,
            submission_id=submission.id
        )

    return redirect(
        "onlinecourse:course_details",
        course_id=course.id
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)

    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__user=request.user,
        enrollment__course=course
    )

    questions = Question.objects.filter(course=course)

    selected_ids = list(
        submission.choices.values_list("id", flat=True)
    )

    total_score = 0
    total_grade = 0

    for question in questions:
        total_grade += question.grade

        if question.is_get_score(selected_ids):
            total_score += question.grade

    percentage = (
        (total_score / total_grade) * 100
        if total_grade > 0 else 0
    )

    context = {
        "course": course,
        "submission": submission,
        "grade": total_score,
        "total_score": total_score,
        "total_grade": total_grade,
        "percentage_score": percentage,
        "choices": submission.choices.all(),
        "selected_ids": selected_ids,
    }

    return render(
        request,
        "onlinecourse/exam_result_bootstrap.html",
        context
    )
