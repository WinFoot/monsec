# -*- coding:utf-8 -*- 
from flask import render_template, flash, redirect
from app import app
from app import db, models
from forms import LoginForm, SheetForm, VulForm, EveForm
from sqlalchemy import func
import datetime
import time
import cgi

def afterday(daystr): #  daystr +10days
    day = datetime.datetime.strptime(daystr, "%Y-%m-%d").date()
    after = day + datetime.timedelta(days=10)
    return str(after)
def today():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))
def month():
    return time.strftime('%Y-%m',time.localtime(time.time()))

@app.route('/')
@app.route('/index')
def index():
    #sheetname = month()
    #return redirect('/report/'+sheetname)
    return report(month())

@app.route('/report/<str_month>')
def report(str_month):
    sheetname = str_month
    mysheet = models.Sheet.query.filter_by(name=sheetname).first()
    if not mysheet:
        flash(u'不存在 ' + sheetname + u'月份报表数据，请创建!')
        return redirect('/sheet')

    vul_history = models.Vul.query.join(models.Sheet, 
                 models.Vul.sheet_id==models.Sheet.id) \
                 .add_columns(models.Sheet.name, func.count('*')).group_by(models.Sheet.name).all()
    vul_history_ret = {}
    for i in vul_history:
        key = '"'+cgi.escape(i[1])+'"' # sheet.name
        val = str(i[2]) # number of vuls
        vul_history_ret[key]=val

    vul_count = models.Vul.query.filter_by(sheet_id=mysheet.id).add_columns(models.Vul.level, func.count("*")).group_by(models.Vul.level).all()
    # {value:2, name:'高危'},
    # {value:1, name:'中危'},
    # {value:0, name:'低危'},
    vul_count_ret = ''
    for i in vul_count:
        key = '"'+cgi.escape(i[1])+'"'
        val = str(i[2])
        vul_count_ret += '{value:'+val+', name:'+key+'},'

    vul_type = models.Vul.query.filter_by(sheet_id=mysheet.id).add_columns(models.Vul.type, func.count("*")).group_by(models.Vul.type).all()
    vul_type_ret = {}
    for i in vul_type:
        key = '"'+cgi.escape(i[1])+'"' # sheet.name
        val = str(i[2]) # number of vuls
        vul_type_ret[key]=val

           # { "name": "03-02 防火墙大量报警ICMP不可达", 
           #     "evolution": [
           #         { "time": "2016-03-02", "value": 10, }, 
           #         { "time": "2016-03-12", "value": 10, },
           #     ] },
    myevent_ret = ''
    for i in mysheet.eves:
        myevent_ret += '{ "name": "'+cgi.escape(i.time)+' '+cgi.escape(i.name)+'", '
        myevent_ret += '    "evolution": ['
        myevent_ret += '        { "time": "'+ cgi.escape(i.time) +'", "value": 10, }, '
        myevent_ret += '        { "time": "'+ cgi.escape(afterday(i.time)) +'", "value": 10, }, '
        myevent_ret += '    ] },'
    

    return render_template('index.html',
        sheet = mysheet,
        vul_history_ret = vul_history_ret,
        vul_count_ret = vul_count_ret,
        vul_type_ret = vul_type_ret,
        myevent_ret = myevent_ret)

@app.route('/dump')
def dump():
    user = { 'nickname': 'Miguel' }
    sheets = models.Sheet.query.all()
    vuls = models.Vul.query.all()
    eves = models.Eve.query.all()
    return render_template('dump.html',
        user = user,
        sheets = sheets,
        vuls = vuls,
        eves = eves)

@app.route('/history')
def history():
    sheets = models.Sheet.query.all()
    return render_template('history.html',
        sheets = sheets,
        title = u'历史')

@app.route('/setting')
def settting():
    #vul = url_for('vul', sheetname=month())
    #eve = url_for('eve', sheetname=month())
    return render_template('setting.html',
        vul   = '/vul/'+month(),
        eve   = '/eve/'+month(),
        title = u'设置')

@app.route('/sheet', methods = ['GET', 'POST'])
def sheet():
    form = SheetForm()
    if form.validate_on_submit():
        u = models.Sheet(name = form.name.data, 
                       level= form.level.data, 
                       timestamp = datetime.datetime.utcnow())
        db.session.add(u)
        db.session.commit()
        flash(u'添加成功: ' + form.name.data)
        return redirect('/sheet')

    form.name.data = month()
    form.level.data = 100
    return render_template('sheet.html', 
        title = u'新建月报',
        form = form)

@app.route('/vul/<sheetname>', methods = ['GET', 'POST'])
def vul(sheetname):
    form = VulForm()
    if form.validate_on_submit():
        mysheet = models.Sheet.query.filter_by(name=sheetname).first()
        u = models.Vul(name = form.name.data, 
                       level= form.level.data, 
                       type = form.type.data, 
                       time = form.time.data, 
                       sheet = mysheet,
                       timestamp = datetime.datetime.utcnow())
        db.session.add(u)
        db.session.commit()
        flash(u'添加成功: ' + form.name.data)
        return redirect('/')

    form.time.data = today()
    return render_template('vul.html', 
        title = u'添加漏洞',
        form = form)

@app.route('/eve/<sheetname>', methods = ['GET', 'POST'])
def eve(sheetname):
    form = EveForm()
    if form.validate_on_submit():
        mysheet = models.Sheet.query.filter_by(name=sheetname).first()
        u = models.Eve(name = form.name.data, 
                       type = form.type.data, 
                       time = form.time.data, 
                       level= form.level.data, 
                       sheet = mysheet,
                       timestamp = datetime.datetime.utcnow())
        db.session.add(u)
        db.session.commit()
        flash(u'添加成功: ' + form.name.data)
        return redirect('/')

    form.time.data = today()
    return render_template('eve.html', 
        title = u'添加事件',
        form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])
