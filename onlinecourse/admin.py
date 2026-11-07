from django.contrib import admin

from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Question,
    Choice,
    Submission,
)


# Inline for adding lessons inside a course
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


# Inline for adding choices inside a question
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


# Inline for adding questions inside a course
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


# Admin configuration for Question
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "course", "grade")
    inlines = [ChoiceInline]
    search_fields = ("question_text",)


# Admin configuration for Lesson
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title",)


# Admin configuration for Course
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "total_enrollment", "pub_date")
    search_fields = ("name",)
    inlines = [LessonInline, QuestionInline]


# Admin configuration for Enrollment
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "date_enrolled", "mode", "rating")
    list_filter = ("mode", "course")


# Register all seven models
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
