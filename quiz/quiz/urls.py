"""
URL configuration for quizzes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

import authentication.views
import quizzes.views




urlpatterns = [
    path("admin/", admin.site.urls),
    # path('', authentication.views.login_page, name='login'),  # the function-based connection view
    # path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.SignupView.as_view(), name='signup'),  # To be a class-based view

    path('', LoginView.as_view(
            template_name='authentication/login.html',
            redirect_authenticated_user=True),
             name='login'),  # Implement login with generic views (class LoginView)

    path('logout/', LogoutView.as_view(
        template_name='authentication/login.html'),
         name='logout'),  # Implement login with generic views (class LogoutView)

    path("password_change/", PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
        name="password_change"),

    path("password_change/done/", PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name="password_change_done",),


    path('home/', quizzes.views.home, name='home'),
    path('quiz/add/', quizzes.views.create_quiz, name='quiz-create'),
    path('quiz/create-multiple/', quizzes.views.create_multiple_quizzes, name='quiz-create-multiple'),
    path('quiz/<int:quiz_id>/', quizzes.views.quiz_view_detail, name='quiz-view-detail'),
    path('quiz/<int:quiz_id>/update|delete', quizzes.views.edit_delete_quiz, name='update-delete-quiz'),
    path('quiz/<int:quiz_id>/deactivate', quizzes.views.deactivate_quiz, name='deactivate-quiz'),

]

# Configuration is used to serve media files in development(DEBUG=1) (like images uploaded by users)
# In production(DEBUG=0), configure a web server like Nginx or Apache to manage media files.
# or to another host a third-party service
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
