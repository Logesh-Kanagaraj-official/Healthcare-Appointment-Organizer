from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    if 'username' not in request.session:
        return redirect('login')
    uname = request.session['username']
    recent = Patent.objects.filter(uname=uname).order_by('-patdt')
    return render(request, 'home.html', {
        'session':      uname,
        'recent_appts': recent[:6],
        'total_appts':  recent.count(),
        'total_docs':   recent.values('docname').distinct().count(),
    })

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        mobno = request.POST.get('mobno')
        email = request.POST.get('email')
        pwrd = request.POST.get('pword')

        if Register.objects.filter(uname=uname).exists():
            data = {'status': "Username already taken. Please choose another."}
            return render(request, 'register.html', context=data)

        reg = Register(uname=uname, mobno=mobno, email=email, pwrd=pwrd)
        reg.save()
        return redirect('index')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwrd = request.POST.get('pwrd')

        # ── Hardcoded Admin ──────────────────────────────────────
        if uname == 'admin' and pwrd == 'admin':
            request.session['username'] = 'admin'
            request.session['is_admin'] = True
            return redirect('admin_dashboard')
        # ────────────────────────────────────────────────────────

        try:
            user = Register.objects.get(uname=uname)
        except Register.DoesNotExist:
            data = {'status': "User not found! Please register first."}
            return render(request, 'login.html', context=data)

        if user.pwrd == pwrd:
            request.session['username'] = uname
            request.session['is_admin'] = False
            return redirect('home')
        else:
            data = {'status': "Incorrect Password!!! Please try again."}
            return render(request, 'login.html', context=data)
    return render(request, 'login.html')


def logout(request):
    if 'username' in request.session:
        del request.session['username']
    if 'is_admin' in request.session:
        del request.session['is_admin']
    return redirect('index')

def patient(request):
    if 'username' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        uname = request.session['username']
        fname = request.POST.get('fname')
        mobno = request.POST.get('mobno')
        email = request.POST.get('email')
        patdt = request.POST.get('patdt')
        docname = request.POST.get('Docname')
        prpse = request.POST.get('prpse')
        pat = Patent(uname=uname, fname=fname, mobno=mobno, email=email,
                     patdt=patdt, docname=docname, prpse=prpse)
        pat.save()
        return redirect('home')
    return render(request, 'patentry.html')

def viewpat(request):
    if 'username' not in request.session:
        return redirect('login')
    d = Patent.objects.filter(uname=request.session['username'])
    data = {'data': d}
    return render(request, 'viewpat.html', context=data)

def admin_dashboard(request):
    """Custom admin dashboard — only accessible by users with is_admin in session"""
    if 'username' not in request.session:
        return redirect('login')
    if not request.session.get('is_admin', False):
        return redirect('home')

    all_appointments = Patent.objects.all().order_by('-patdt')
    all_users        = Register.objects.all().order_by('id')
    latest           = all_appointments.first()

    data = {
        'appointments':       all_appointments,
        'users':              all_users,
        'total_appointments': all_appointments.count(),
        'total_users':        all_users.count(),
        'total_doctors':      all_appointments.values('docname').distinct().count(),
        'latest_date':        latest.patdt if latest else None,
        'admin_name':         request.session['username'],
    }
    return render(request, 'admin_dashboard.html', context=data)