from .models import friend,Category,Table
from django.shortcuts import render,redirect,HttpResponse
from datetime import datetime





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


def friends(request):
    datas =friend .objects.filter(Status=False)
    return render(request, 'friendrequest.html', {'value': datas})

def friendaccept(id):
    user = friend.objects.get(id=id)
    user.Status = True
    user.save()
    return redirect('/friend')
def frienddelete(id):
    friend.objects.get(id=id).delete()
    return redirect('/friend')
def debit(request,username):
    if request.method == 'POST':
        User = username
        Debit = float(request.POST.get('debit'))
        users = Table()
        users.User = User
        users.Category = "Income"
        users.Debit = Debit
        users.Credit = 0
        users.Getback = 0
        last_rowb = Table.objects.exclude(Balance=None).last()
        if last_rowb is None:
            balance = float(0)
            debit_balance = float(0)
        else:
            balance = float(last_rowb.Balance)
            debit_balance = float(last_rowb.Debit_Balance)
        users.Balance=Debit+balance
        users.Debit_Balance = Debit + debit_balance
        users.save()
    return render(request,'debitadd.html')
def getback(request,username):
    if request.method == 'POST':
        User = username
        getback = float(request.POST.get('back'))
        users = Table()
        users.User = User
        users.Category = "Getback"
        users.Debit = 0
        users.Credit = 0
        users.Getback = getback
        last_rowb = Table.objects.exclude(Balance=None).last()
        if last_rowb is None:
            balance = float(0)
            debit_balance = float(0)
        else:
            balance = float(last_rowb.Balance)
            debit_balance=float(last_rowb.Debit_Balance)
        users.Balance=balance
        users.Debit_Balance =  debit_balance -getback
        users.save()
    return render(request,'getback.html')
def credit(request,username):
    a= Category.objects.all()
    if request.method == 'POST':
        User = username
        Categorys = request.POST.get('category')
        credit = float(request.POST.get('credit'))
        users = Table()
        users.User = User
        users.Category = Categorys
        users.Credit = credit
        users.Debit = 0
        users.Getback = 0
        last_rowb = Table.objects.exclude(Balance=None).last()
        if last_rowb is None:
            balance =float(0)
            debit_balance = float(0)
        else:
            balance =float(last_rowb.Balance)
            debit_balance = float(last_rowb.Debit_Balance)
        count = friend.objects.all()
        count = len(count)
        remain=count-1
        credit_balance=(remain/count)*credit
        users.Balance =  balance - credit_balance
        users.Debit_Balance=debit_balance
        users.save()
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
    data=Table.objects.all()
    debit = Table.objects.filter(User=username).values_list('Debit', flat=True)
    credit= Table.objects.exclude(User=username).values_list('Credit', flat=True)
    debit_sum = float(sum(debit))
    credit_sum = float(sum(credit))
    count = friend.objects.all()
    count=len(count)
    credit_balace=credit_sum/count
    balance=debit_sum-credit_balace
    #
    credit = Table.objects.filter(User=username).values_list('Credit', flat=True)
    getback = Table.objects.filter(User=username).values_list('Getback', flat=True)
    credit_sum = float(sum(credit))
    if getback is None:
        getback_sum=float(0)
    else:
        getback_sum = float(sum(getback))

    remain = count - 1
    credit_balance = float((remain / count) * credit_sum)
    extra=credit_balance-getback_sum
    return render(request, 'friendpage.html',{'username':username,'value':data,'balance':balance,'get_back':extra})
def transcdelete(id):
    Table.objects.get(id=id).delete()
    latest_record = Table.objects.all().order_by('-id').first()
    if latest_record is not None:
        lid = latest_record.id
        id = id + 1
        for id in range(id, lid + 1):
            try:
                record = Table.objects.get(id=id)
                credit = float(record.Credit)
                getback = float(record.Getback)
                count = friend.objects.all()
                count = len(count)
                remain = count - 1
                credit_balance = float((remain / count) * credit)
                debit = float(record.Debit)
                previous = Table.objects.filter(id__lt=id).order_by('-id').values('Balance').first()
                previous_debit_balance = Table.objects.filter(id__lt=id).order_by('-id').values('Debit_Balance').first()
                if previous is None:
                    balance = float(0)
                    debit_balance = float(0)
                else:
                    balance = float(previous['Balance'])
                    debit_balance = float(previous_debit_balance['Debit_Balance'])
                record.Balance = balance - credit_balance + debit
                record.Debit_Balance = debit_balance + (debit-getback)
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

        if method=='Debit':
            debit=amount
            credit = 0
            credit_balance=0
            getback=0
            data.Category="Income"
        elif method=='Credit':
            credit=amount
            count = friend.objects.all()
            count = len(count)
            remain = count - 1
            credit_balance = float((remain / count) * credit)
            debit = 0
            getback = 0
            data.Category = category
        elif method=='Getback':
            debit=0
            credit = 0
            getback = amount
            data.Category = "Getback"

            credit_balance=0
        data.Credit = credit
        data.Debit = debit
        data.Getback=getback
        latest_record = Table.objects.filter(id__lt=id).order_by('-id').values('Balance').first()
        latest_debit_balance = Table.objects.filter(id__lt=id).order_by('-id').values('Debit_Balance').first()
        if latest_record is None:
            balance=float(0)
            debit_balance = float(0)
        else:
            balance = float(latest_record['Balance'])
            debit_balance = float(latest_debit_balance['Debit_Balance'])

        data.Balance =(balance-credit_balance)+debit
        data.Debit_Balance = debit_balance + debit - getback
        data.save()
        latest_record = Table.objects.all().order_by('-id').first()
        lid = latest_record.id
        id=id+1
        for id in range(id,lid+1) :
            try:
                record = Table.objects.get(id=id)
                credit =float(record.Credit)
                getback = float(record.Getback)
                count = friend.objects.all()
                count = len(count)
                remain = count - 1
                credit_balance = float((remain / count) * credit)
                debit = float(record.Debit)
                previous = Table.objects.filter(id__lt=id).order_by('-id').values('Balance').first()
                previous_debit_balance = Table.objects.filter(id__lt=id).order_by('-id').values('Debit_Balance').first()
                if latest_record is None:
                    balance =float(0)
                    debit_balance = float(0)
                else:
                    balance = float(previous['Balance'])
                    debit_balance = float(previous_debit_balance['Debit_Balance'])
                record.Balance = balance  - credit_balance + debit
                record.Debit_Balance = debit_balance  + (debit - getback)
                record.save()
            except:
                continue

        return redirect('/adminpage/Admin')
    return render(request,'transedit.html',{'value':details,'a':data,'values':cat})

def adminpage(request,username):
    datas = Table.objects.all()
    data = Category.objects.all()
    date = Table.objects.values_list('Date', flat=True).distinct()
    credit = Table.objects.values_list('Credit', flat=True)
    credit_sum = sum(credit)

    if request.method == 'POST':

        selected_options = request.POST.getlist('option')
        selected_option = request.POST.getlist('dates')
        selected_optione = [datetime.strptime(date, "%b. %d, %Y").strftime("%Y-%m-%d") for date in selected_option]
        dat = Table.objects.filter(Category__in=selected_options) | Table.objects.filter(Date__in=selected_optione)
        credit = dat.values_list('Credit', flat=True)
        credit_sum = sum(credit)
        return render(request, 'filter.html', {'value': dat, 'a': data,'username':username,'date':date,'expenses':credit_sum})


    return render(request, 'filter.html', {'value': datas,'a':data,'username':username,'date':date,'expenses':credit_sum})