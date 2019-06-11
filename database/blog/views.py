from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.db import connection

from blog.models import Article

from django.shortcuts import redirect 
from collections import namedtuple
import json
# def index(request):
#     cursor = connection.cursor()

#     # cursor.execute( "insert into book values ('1','xietianqi')" )

#     cursor.execute( "select * from book ")
#     rows = cursor.fetchall()
#     for cow in rows:
#         print(cow[1])

#     return HttpResponse('hello, world!')

# 登录
def show_login(request):
    return render(request, 'login.html')

# 注册
def show_register(request):
    return render(request, 'register.html')

# 个人信息
def person_info(request):
    return render(request, 'edit.html')

def show_insert(request):
    return render(request, 'insert.html')

def delete(request):
    username = request.COOKIES['username']
    if (request.method == 'POST'):
        delete_content = request.POST.get('delete')

        flag = 0
        cursor = connection.cursor()
        select_all = 'select username from info'
        cursor.execute(select_all)
        selected = cursor.fetchall()
        for row in selected:
            if(row[0] == username):
                print(row[0])
                flag = 1
                break
        if(flag == 1):
            print(1)
            if(delete_content == '立即删除'):
                mysql = 'delete from info where username = ' + '\'' + str(username) + '\''
                cursor.execute(mysql)
                return render(request, 'login.html')
            else:
                return render(request, 'delete.html',{
                    'username' : username,
                    'message' : 'input wrong'
                })
        else:
            print(2)
            return render(request, 'login.html')
    else:
        return render(request, 'delete.html', { 
            'username' : username,
            'message' : ''
        })

# 登录
def login(request):
    # 获取所有的文件信息
    article_list = Article.objects.all()

    # flag是0表示没有账号密码输入错误
    flag = 0

    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

    cursor = connection.cursor()
    cursor.execute("select * from info")
    infos = cursor.fetchall()
    
    for row in infos:
        if(row[0] == username and row[1] == password):
            flag = 1
            break


    # 转页
    if(flag == 0):

        return render(request, 'login.html', 
        {
            'username' : username,
            'message' : '请输入正确的账号密码'
        })
    else:
        # return render(request, 'index.html', 
        #     {
        #         'article_list': article_list
        #     })
        response = redirect('/blog/index')
        response.set_cookie('username',username,max_age=3600)
        return response


# 注册
def register(request):


    # 获取信息
    if (request.method == 'POST'):
        print(1)
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm  = request.POST.get('confirm')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # 转换页面
        if(str(confirm) != str(password)):
            return render(request, 'register.html',{
                "message" : "两次输入的密码不同"
            })
        else:
            # 向数据库插入数据
            cursor = connection.cursor()
            mysql = "insert into info values" + "(" + "\'" + str(username) + "\'" + "," \
                + "\'" + str(password) + "\'" + ',' + "\'" + str(email) + "\'" + ',' + "\'" + str(phone) + "\'" +")"
            cursor.execute(mysql)
            # print(mysql)
            return render(request, 'login.html')
    else:
        return render(request, 'register.html')



# 主页
def index(request):
    article_list = Article.objects.all()
    # for article in article_list:
    #     print(article.title)
    if 'username' in request.COOKIES:
        # 获取记住的用户名
        username = request.COOKIES['username']
    else:
        username = ''

    return render(request, 'index.html', 
    {
        'article_list': article_list,
    })



# 精准页
def get_detail_page(request, article_id):

    if(request.method == 'POST'):
        comment = request.POST.get('comment')


        if(comment != ''):
            username = request.COOKIES['username']
            cursor1 = connection.cursor()
            
            sentence = 'select email from info where username = ' + "\'" + str(username) + "\'"

            print(sentence)
            cursor1.execute(sentence)
            email_all = cursor1.fetchall()
            for row in email_all:
                email = row[0]
            
            print(email)
            
            
            sentence1 = 'insert into comment values (' + "\'" + str(username) + "\'" + ',' \
                + "\'" + str(comment) + "\'" + ',' + "\'" + str(email) + "\'" + ',' + str(article_id) + ')'
            print(sentence1)
            cursor1.execute(sentence1)



    # 获取所有文章信息
    all_article = Article.objects.all()
    curr_article = None

    # 取当前文章
    for article in all_article:
        # print(article.article_id)
        if(article.article_id == article_id):
            curr_article = article
            break
    
    # 输出的时候讲文章分段
    section_list = curr_article.content.split('\n')
    article_list = Article.objects.all()
    # for article in article_list:
    #     print(article.title)

    
    cursor = connection.cursor()
    mysql = 'select * from comment where article_id = ' + str(article_id)
    cursor.execute(mysql)


    com_info = namedtuple('User',['name', 'comment', 'email'])
    comment_list = []
    comment_all = cursor.fetchall()
    for signal_comment in comment_all:
        temp = com_info(name = signal_comment[0], comment = signal_comment[1], email = signal_comment[2])
        comment_list.append(temp)


    return render(request , 'detail.html',
    {
        'section_list': section_list,
        'curr_article': curr_article,
        'comment_list' : comment_list,
        'article_list' : article_list
    })




# 修改个人信息
def edit(request):
    # curr_user = request.user
    # print(curr_user)
    ## 获取当前登录的用户名
    username = request.COOKIES['username']

    ## confirm为再次输入密码
    password = None
    confirm = '1'
    # confirm = '1'
    email = ''
    phone = ''

    ## 获取密码和重复输入的密码
    if (request.method == 'POST'):
        password = request.POST.get('new_password')
        confirm  = request.POST.get('confirm')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

    ## 在数据库之中查找有无此用户
    search = 'select username from info'
    cursor = connection.cursor()
    cursor.execute(search)

    # flag代表存在此用户
    flag = 0
    info_user = cursor.fetchall()
    for user in info_user:
        if(user[0] == username):
            flag = 1
            break
    
    ## 成功和失败的输出
    if(flag == 1):
        if(password == confirm):

            # 执行sql语句
            mysql = 'update info set password = ' + "\'" + str(password) + "\'"
            if(email != ''):
                mysql = mysql + ',' + 'email = ' + "\'" + str(email) + "\'"
            if(phone != ''):
                mysql = mysql + ',' + 'phone = ' + "\'" + str(phone) + "\'"
            mysql = mysql + " where username = " + "\'" + str(username) + "\'"
            cursor.execute(mysql)
            return render(request, 'edit.html', {
                'username' : username,
                'message' : '修改成功，新密码为'+str(password)
            })
        
        # 两次密码输入不一致
        else:
            if(password == None and confirm == '1'):
                return render(request, 'edit.html', {
                    'username' : username,
                    'message' : ''
                })
            else:    
                return render(request, 'edit.html', {
                    'username' : username,
                    'message' : '两次密码不一致'
                })

    # 不存在此用户
    if(flag == 0):
        return render(request, 'edit.html',{
            'message' : '请输入正确的账号'
        }
        )


def insert(request):
    if (request.method == 'POST'):
        print(1)
        title = request.POST.get('title')
        brief_content = request.POST.get('brief_content')
        content = request.POST.get('content')

        a = Article()
        a.title = title
        a.brief_content = brief_content
        a.content = content
        a.save()

        return render(request, 'insert.html')
    else:
        print(2)
        return render(request, 'insert.html')