
from .models import friend,Category,Table
from django.shortcuts import render,redirect,HttpResponse




def registerpage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = friend()
        users.Name = name
        users.Address = address
        users.Username = username
        users.Password = password
        users.save()

    return render(request,'registerpage.html')

def categoryadd(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')

        users = Category()
        users.User = name
        users.Category = category

        users.save()

    return render(request,'categoryadd.html')

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'Admin' and password == '1':
            return redirect('/adminpage/'+username)
        else:
            return HttpResponse('invalid ')
    return render(request,'adminlogin.html')

def adminpage(request,username):
    datas = Table.objects.all()
    return render(request, 'adminpage.html', {'value': datas,'username':username})

def friends(request):
    datas =friend .objects.filter(Status=False)
    return render(request, 'friendrequest.html', {'value': datas})

def friendaccept(request,id):
    user = friend.objects.get(id=id)
    user.Status = True
    user.save()
    return redirect('/friend')
def frienddelete(request,id):
    friend.objects.get(id=id).delete()
    return redirect('/friend')
def debit(request,username):
    a= Category.objects.all()
    if request.method == 'POST':
        User = username
        Debit = request.POST.get('debit')
        users = Table()
        users.User = User
        users.Description = "None"
        users.Category = "Income"
        users.Debit = Debit
        users.Credit = 0
        users.save()
        last_rowd = Table.objects.last()
        debit = last_rowd.Debit

        last_rowb = Table.objects.exclude(Balance=None).last()
        if last_rowb is None:
            balance = 0
        else:
            balance = last_rowb.Balance
        last_row = Table.objects.last()
        last_row.Balance=debit+balance
        last_row.save()
    return render(request,'debitadd.html',{'value':a})
def credit(request,username):
    a= Category.objects.all()
    if request.method == 'POST':
        User = username
        Categorys = request.POST.get('category')
        credit = request.POST.get('credit')
        description = request.POST.get('description')
        users = Table()
        users.User = User
        users.Description = description
        users.Category = Categorys
        users.Credit = credit
        users.Debit = 0
        users.save()
        last_rowd = Table.objects.last()
        credit = last_rowd.Credit

        last_rowb = Table.objects.exclude(Balance=None).last()
        if last_rowb is None:
            balance = 0
        else:
            balance = last_rowb.Balance
        last_row = Table.objects.last()
        last_row.Balance = balance - credit
        last_row.save()
    return render(request,'creditadd.html',{'value':a})

def friendlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            friend.objects.get(Username=username,Password=password,Status=True)
            return redirect('/friendpage/'+username)
        except:
            return HttpResponse('invalids user')

    return render(request,'friendlogin.html')
def friendpage(request,username):
    return render(request, 'friendpage.html',{'username':username})
def transcdelete(request,id):
    Table.objects.get(id=id).delete()
    latest_record = Table.objects.all().order_by('-id').first()
    lid = latest_record.id
    id = id + 1
    for id in range(id, lid + 1):
        try:
            record = Table.objects.get(id=id)
            credit = record.Credit
            debit = record.Debit
            previous = Table.objects.filter(id__lt=id).order_by('-id').values('Balance').first()
            if latest_record is None:
                balance = 0
            else:
                balance = previous['Balance']
            balance = balance + debit - credit
            record.Balance = balance
            record.save()
        except:
            continue
    return redirect('/adminpage/Admin')

def transedit(request,id):
    cat=Category.objects.all()
    details = Table.objects.filter(id=id)
    data = Table.objects.get(id=id)
    if request.method =='POST':
        category=request.POST.get('category')
        method=request.POST.get('method')
        amount = int(request.POST.get('amount'))
        data.Category=category
        if method=='Debit':
            debit=amount
            credit = 0
        elif method=='Credit':
            credit=amount
            debit = 0
        data.Credit = credit
        data.Debit = debit
        latest_record = Table.objects.filter(id__lt=id).order_by('-id').values('Balance').first()
        if latest_record is None:
            balance=0
        else:
            balance = latest_record['Balance']
        data.Balance=((balance-credit)+debit)
        data.save()
        latest_record = Table.objects.all().order_by('-id').first()
        lid = latest_record.id
        id=id+1
        for id in range(id,lid+1) :
            try:
                record = Table.objects.get(id=id)
                credit = record.Credit
                debit = record.Debit
                previous = Table.objects.filter(id__lt=id).order_by('-id').values('Balance').first()
                if latest_record is None:
                    balance = 0
                else:
                    balance = previous['Balance']
                balance = balance + debit - credit
                record.Balance = balance
                record.save()
            except:
                continue

        return redirect('/adminpage/Admin')
    return render(request,'transedit.html',{'value':details,'a':data,'values':cat})

