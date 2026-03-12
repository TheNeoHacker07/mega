# apps/books/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from apps.books.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_new_books_notification():
    last_day = now() - timedelta(hours=24)
    books = Book.objects.filter(created_at__gte=last_day)

    if not books.exists():
        return "No new books in last 24h"

    book_titles = "\n".join([book.title for book in books])
    subject = "New books added in the last 24 hours"
    message = f"Hello! Here are the new books:\n{book_titles}"

    recipients = User.objects.filter(is_active=True).values_list('email', flat=True)
    send_mail(subject, message, 'noreply@yourdomain.com', recipients)
    return f"Sent notifications to {len(recipients)} users"

@shared_task
def send_anniversary_books():
    today = now().date()
    books = Book.objects.filter(publication_date__month=today.month, publication_date__day=today.day)

    if not books.exists():
        return "No anniversaries today"

    book_titles = "\n".join([book.title for book in books])
    subject = "Book anniversaries today!"
    message = f"Hello! Today is the anniversary of these books:\n{book_titles}"

    recipients = User.objects.filter(is_active=True).values_list('email', flat=True)
    send_mail(subject, message, 'noreply@yourdomain.com', recipients)
    return f"Sent anniversary notifications to {len(recipients)} users"