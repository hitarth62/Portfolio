from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from .models import Project, Contact

# Create your views here.
def home(request):
    projects = Project.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save contact in DB
        contact = Contact(name=name, email=email, message=message)
        contact.save()

        # Success message for UI
        messages.success(request, f"Thank you {name}, we’ve received your message!")

        # --- Auto-reply to visitor (HTML email with CSS) ---
        subject_user = "Thank You for Contacting Hitarth Patel"
        html_message_user = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f6f9;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: white;
                    border-radius: 12px;
                    padding: 30px;
                    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
                    animation: fadeIn 1.2s ease-in-out;
                }}
                h2 {{
                    color: #4CAF50;
                    text-align: center;
                    animation: slideDown 1s ease-in-out;
                }}
                p {{
                    font-size: 16px;
                    color: #333;
                    line-height: 1.6;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 14px;
                    color: #777;
                    text-align: center;
                }}
                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(20px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                @keyframes slideDown {{
                    from {{ transform: translateY(-30px); opacity: 0; }}
                    to {{ transform: translateY(0); opacity: 1; }}
                }}
                .btn {{
                    display: inline-block;
                    background: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 6px;
                    margin-top: 15px;
                    transition: background 0.3s;
                }}
                .btn:hover {{
                    background: #43a047;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Thank You, {name}!</h2>
                <p>Hello {name},</p>
                <p>Thank you for reaching out through my portfolio website.</p>
                <p>I’ve received your message and will get back to you as soon as possible.</p>
                <p>Meanwhile, feel free to explore more of my work:</p>
                <a href="https://your-portfolio-link.com" class="btn">View My Projects</a>
                <div class="footer">
                    <p>Best regards,<br><b>Hitarth Patel</b><br>Web Developer | Video Editor</p>
                </div>
            </div>
        </body>
        </html>
        """

        email_user = EmailMessage(
            subject_user,
            html_message_user,
            settings.EMAIL_HOST_USER,
            [email]
        )
        email_user.content_subtype = "html"
        email_user.send()

        # --- Notification email to you (plain text is fine) ---
        subject_owner = f"New Contact Form Submission from {name}"
        message_owner = (
            f"New message received via portfolio contact form:\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Message:\n{message}\n\n"
            f"Check your admin panel for details."
        )
        send_mail(subject_owner, message_owner, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])

    return render(request, 'home.html', {'projects': projects})
