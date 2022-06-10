from email import message
from flask import Flask, redirect,render_template,request,session
app=Flask(__name__)
app.config['SECRET_KEY']='1234'

#building the route
@app.route('/')
def home():
    return redirect('/register')
    name='Dhruv'
    location='India'
    session['my_name']=name #session={'my_name':'Dhruv'}
    session['place']=location
    return '''<h1 style="color:red;"> Home'''

@app.route('/aboutme')
def aboutme():
    return '''This is about me!!!'''


@app.route('/evenorodd')
def evenorodd():
    return render_template('evenorodd.html')   

@app.route('/validate_evenorodd')
def validate_evenodd():
    number=int(request.args.get('number'))
    result=''
    if number%2==0:
       result="Even Number"
    elif number%2!=0:
       result="Odd Number"
    return render_template('evenorodd.html',output=result)

@app.route('/max_num')
def max_num():
    return render_template('max.html')

@app.route('/validate_max')
def validate_max():
    n1=int(request.args.get('num1'))
    n2=int(request.args.get('num2'))
    n3=int(request.args.get('num3'))
    result=''
    if n1>n2 and n1>n3:
        result='num1 is the greatest among 3'
    elif n2>n3 and n2>n1:
        result='num2 is the greatest among 3'
    elif n3>n2 and n3>n1:
        result='num2 is the greatest among 3'
    return render_template('max.html',result=result)
    
@app.route('/get_character')
def get_character():
    return render_template('character.html')

@app.route('/character')
def character():
    if session.get('authenticated')!= True:
        return redirect ('/login')
    character=request.args.get('char')
    ord_value=ord(character)

    # lowercase  a-97  z-122
    if ord_value>=97 and ord_value<=122:
        result= 'The entered data is a lowercase alphabet'

    # uppercase  A-65  Z-99
    elif ord_value>=65 and ord_value<=99:
        result= 'The entered data is a uppercase alphabet'

    # numbers  0-48  9-57
    elif ord_value>=48 and ord_value<=57:
        result= 'The entered data is a number'

    # special charcaters
    else:
       result= 'The entered data is a punctuation or symbol'

    return render_template('character.html',result=result)

@app.route('/l_b')
def l_b():
    length=int(request.args.get('length'))
    breadth=int(request.args.get('breadth'))
    if length==breadth:
        result='square'
    else:
        result='rectangle'
    return render_template('l_b.html',result=result)

emails=['user1@gmail.com','user2@gmail.com','user3@gmail.com']
passwords=[123,456,789]


@app.route('/register',methods=["GET",'POST'])
def validate_register():
    if request.method=='GET':
        name=session.get('my_name', 'user')
        message='Hello ' +name+  ' ,Welcome to the Registration page'
        return render_template('register.html', message=message)
    elif request.method=='POST':       
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        age=int(request.form.get('age'))

        # Check whether email is already present in the list
        if email in emails:
            message='Email Id already exist'
        elif email not in emails:
            if age>=12:
                message='Hi ' +name+ ' ,Registered Successfully'
                emails.append(email)
                passwords.append(password)
                session['my_email']=email
                session['my_password']=password
            else:
                message='Not eligible for registration'
        return render_template('register.html',message=message)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        email_session=session.get('my_email')
        password_session=session.get('my_password')
        message=''
        if email==email_session and password==password_session:
            message='Login Successful'
            session['authenticated'] =True
            return render_template('home.html',message)
        else:
            message='Either email or password is incorrect'
            return render_template('login.html',message==message)
        

@app.route('/question1', methods=['GET', 'POST'])
def question1():
    score=session.get('score',0)
    #user not logged in
    #if session.get('authenticated')!=True:#session={'authenticated':True}
       # return redirect("/register")
    if request.method=='GET':
        return render_template('question1.html')
    elif request.method=='POST':
        correct_answer='b'
        user_option=request.form.get('option')
        message=''
        if user_option==correct_answer:
            message='Your answer is correct'
            score=score+10
            session['score']=10 #10
        else:
            message='Your answer is wrong, The right answer is 1960' #0
    return render_template('question1.html',message=message)

@app.route('/question2', methods=['GET', 'POST'])
def question2():
    score=session.get('score',0)
    if request.method=='GET':
        return render_template('question2.html')
    elif request.method=='POST':
        correct_answer='d'
        user_option=request.form.get('option')
        message=''
        if user_option==correct_answer:
            message='Your answer is correct'
            score=score+10
            session['score']=score
        else:
            message="Your answer is wrong, the right answer is Muggles can't see the Knight Bus"
    return render_template('question2.html',message=message) 

@app.route('/question3', methods=['GET', 'POST'])
def question3():
    score=session.get('score',0)
    if request.method=='GET':
        return render_template('question3.html')
    elif request.method=='POST':
        correct_answer='c'
        user_option=request.form.get('option')
        message=''
        if user_option==correct_answer:
            message='Your answer is correct'
            new_score=score+10
            #replacing new score in session
            session['score']=new_score
        else:
            message='Your answer is wrong, the right answer is Seeker'
    return render_template('question3.html',message=message) 

@app.errorhandler(404)
def page_not_found(e):
    #note that we set the 404 status explicitly
    return render_template('404.html'), 404 

leaderboard=[[1,'test1','test1@gmail.com',60],
            [1,'test1','test1@gmail.com',59],
            [1,'test1','test1@gmail.com',58],
            [1,'test1','test1@gmail.com',57],
            [1,'test1','test1@gmail.com',56],]
@app.route('/leaderboard')
def leaderboard_data():
    return render_template('leaderboard.html',leaderboard=leaderboard)
if __name__=='__main__':
    app.run(debug=True)
 