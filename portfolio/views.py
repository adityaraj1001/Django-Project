from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Profile, Project, ContactMessage

def home(request):
    """
    Public Home Page: Fetches profile details and ordered projects. [cite: 89, 90]
    """
    profile = Profile.objects.first()
    # Corrected field name to 'created_at' and added ordering as per source 183
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'home.html', {
        'profile': profile,
        'projects': projects
    })

def projects_list(request):
    """
    Public Projects Page: Lists all projects ordered by newest first. [cite: 101, 183]
    """
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects.html', {'projects': projects})

def project_detail(request, slug):
    """
    Project Detail Page: Retrieves a specific project by its slug. [cite: 64, 102]
    """
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'project_detail.html', {'project': project})

def contact(request):
    """
    Contact Form: Handles database storage and dual-email notification. [cite: 71, 72]
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Saves submission to PostgreSQL database [cite: 135]
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        # Notification to Admin [cite: 190]
        send_mail(
            subject=f"New Portfolio Message from {name}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=True,
        )

        # Confirmation to User [cite: 191]
        send_mail(
            subject="Thank you for contacting Aditya Raj",
            message=f"Hi {name},\n\nThank you for reaching out through my portfolio website.\n\nI have received your message and will get back to you as soon as possible.\n\nBest regards,\nAditya Raj\nFull Stack Developer | Django | ML",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=True,
        )

        return redirect('home')

    return render(request, 'contact.html')

def signup_view(request):
    """
    Signup Page: Allows new users to register. [cite: 109]
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required # Restricts access to authenticated users only [cite: 66, 116]
def dashboard(request):
    """
    Admin Dashboard: Protected view to manage projects and read messages. [cite: 65, 113]
    """
    projects = Project.objects.all().order_by('-created_at')
    # Orders messages by newest timestamp 
    messages = ContactMessage.objects.all().order_by('-timestamp')
    return render(request, 'dashboard.html', {
        'projects': projects,
        'messages': messages
    })