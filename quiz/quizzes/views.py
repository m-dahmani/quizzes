from django.contrib.auth.decorators import login_required, permission_required
from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404

from .forms import QuizForm, DeleteQuizForm
from .models import Quiz


# the function-based connection view
@login_required  # Restrict access to the home page and by default setting.LOGIN_URL = 'login'
def home(request):
    # Take a look at « request.user»  »
    user = request.user
    print(user.get_all_permissions())  # Return the user permissions
    print(user.has_perm('quiz.add_quiz'))  # Return True for the quizmasters False for the notquizmasters
    print(user.has_perm('quiz.change_quiz'))   # Return True for the quizmasters False for the notquizmasters
    print(user.has_perm('quiz.deactivate_quiz'))   # Return True for the moderators False for the quizmasters

    quizzes = Quiz.objects.all()  # recover the instances(quiz) in the home page
    return render(request, 'quizzes/home.html', {'quizzes': quizzes})


@login_required  # Restrict access to the user connected
@permission_required('quiz.add_quiz', raise_exception=True)  # to limit access based on permission
def create_quiz(request):
    # Take a look at « request.method » and « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    print('Les données login : ', request.user)
    print('Les données Media : ', request.FILES)

    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)  # pass data & images(FILES) to form
        if form.is_valid():
            quiz = form.save(commit=False)  # to not save the object in the database with commit=False
            # Initialize & set the author to the user connected before saving the model
            quiz.author = request.user  # assign a value to the uploader field: we will put the user connected
            # now we can save
            quiz.save()  # save the quiz in the DB
            return redirect('home')

    else:
        form = QuizForm()  # get the quizForm()

    return render(request, 'quizzes/create_quiz.html', context={'form': form})  # to pass it to the template


@login_required       # Restrict access to the user connected
@permission_required(['quizzes.add_quiz'], raise_exception=True)
def create_multiple_quizzes(request):  # create a view that allows you to create multiple quizzes at once
    # This approach allows you to manage multiple quiz forms on the same page in a clean and efficient way.
    # use the formset_factory method to create and generate a class that will be our FormSet
    QuizFormSet = formset_factory(QuizForm, extra=3)  # extra=3 == the number of instances # 3 forms by default,
    # adjust as needed
    formset = QuizFormSet()  # we instantiate the class

    # Take a look at « request.method » and « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    print('Les données login : ', request.user)
    print('Les données Media : ', request.FILES)

    if request.method == 'POST':

        formset = QuizFormSet(request.POST, request.FILES)

        if formset.is_valid():
            for form in formset:  # iterate through each form in Formset
                # for each Formset form, we will check if there is data in it
                # (because even if the form is valid, one or more forms are empty, they must be ignored)
                if form.cleaned_data:  # This allows you to check the current form, we have data that is not empty
                    # and in this case, we can manage it
                    quiz = form.save(commit=False)
                    # The templates do not need additional author-specific modifications
                    # since this field is populated in the background in the view.
                    quiz.author = request.user  # assign the author field to the request user
                    quiz.save()  # we will save the quiz

            return redirect('home')  # outside the loop we will return the redirection to the home page

    return render(request, 'quizzes/create_multiple_quizzes.html', {'formset': formset})


@login_required
# @permission_required('quizzes.delete_quiz', raise_exception=True)
@permission_required(['quizzes.change_quiz'], raise_exception=True)
def edit_delete_quiz(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Initialise par défaut pour éviter l'erreur UnboundLocalError je pense en cas d'oublier DeleteQuizForm(forms.Form):
    # La variable edit_form est initialisée au début de la vue, avant de vérifier le type de requête (GET ou POST).
    # Cela garantit qu'elle est toujours définie et empêche l'erreur UnboundLocalError.
    # edit_form = QuizForm(instance=quiz)

    # Take a look at « request.method » and « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    print('Les données login : ', request.user)

    if request.method == 'POST':
        # check which form is sent by checking the presence of this field (edit_quiz) in the POST data
        if 'edit_quiz' in request.POST:
            # we pre-fill the form with an existing quiz the instance already created and fill it with the POST data
            edit_form = QuizForm(request.POST, instance=quiz)
            if edit_form.is_valid():
                # update the instance of the object already created “quiz” and save it in the database
                edit_form.save()
                # return redirect('home')
                # redirect to the detail page of the quiz we just update
                return redirect('quiz-view-detail', quiz.id) # ok

        # check which form is sent by checking the presence of this field (delete_quiz) in the POST data
        elif 'delete_quiz' in request.POST:
            # Debug
            # Add debug messages
            print('Delete quiz POST detected')

            if 'confirm' in request.POST:
                # Debug
                print('Delete confirm POST detected')
                # Create an instance of our form and fill it with the POST data
                # delete_form = DeleteQuizForm(request.POST)  # ??? no need this
                # if delete_form.is_valid():  # ??? no need this
                # delete the quiz object in the database
                quiz.delete()
                # Debug
                print('Quiz successfully deleted')
                # redirect to the list-page of the quiz we just verified if existing it
                return redirect('home')  # Nok  ??

            elif 'cancel' in request.POST:
                # Debug
                print('Delete cancel POST detected')
                # redirect to the list-page of the quiz we just verified if existing it
                return redirect('home')  # Nok ???
            else:
                # Debug
                print('Neither confirm nor cancel detected')
        else:
            # Debug
            print('Neither edit_quiz nor delete_quiz in POST data => on entre ici '
                  'car on a oublié héritage DeleteQuizForm(forms.Form):')

    else:
        # we pre-fill the form with an existing quiz the instance already created
        # this must be a GET request, so open with the instance of the object already created
        edit_form = QuizForm(instance=quiz)
        # this must be a GET request, so create an empty form
        delete_form = DeleteQuizForm()  # Add a new DeleteQuizForm empty here if request.GET

    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'quizzes/edit_delete_quiz.html', context)


# Create the view to disable quizzes
@permission_required('quizzes.deactivate_quiz', raise_exception=True)  # to limit access based on permission
def deactivate_quiz(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Take a look at « request.method » and « request.POST »
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    print('Les données login : ', request.user)
    print(quiz.is_active)

    if request.method == 'POST':
        quiz.is_active = False
        quiz.save()
        # Debug
        print(quiz.is_active)
        return redirect('home')  # ok

    return render(request, 'quizzes/deactivate_quiz.html', {'quiz': quiz})


@login_required
def quiz_view_detail(request, quiz_id):
    # to recover the quiz(obj) and handle the case where the object does not exist.
    quiz = get_object_or_404(Quiz, id=quiz_id)
    context = {'quiz': quiz}
    return render(request, 'quizzes/quiz_view_detail.html', context)


