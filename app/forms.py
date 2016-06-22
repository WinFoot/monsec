# -*- coding:utf-8 -*- 
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)
    
class SheetForm(Form):
    name = StringField(u'月报名称(例：2016-01)', validators = [DataRequired()])
    level = IntegerField(u'风险指数', validators = [DataRequired()])

class VulForm(Form):
    name = StringField(u'漏洞名称', validators = [DataRequired()])
    time = StringField(u'发现时间(例：2016-01)')
    type = SelectField(u'漏洞类型', choices=[('sqli', u'SQL注入'), ('xss', u'跨站脚本'), ('weekpass', u'弱口令')])
    level = SelectField(u'漏洞等级', choices=[('high', u'高危'), ('middle', u'中危'), ('low', u'低危')])

class EveForm(Form):
    name = StringField(u'事件名称', validators = [DataRequired()])
    time = StringField(u'发生时间(例：2016-01)')
    type = SelectField(u'事件类型', choices=[('riskmanage', u'反垃圾和风控'),('ddostattack', u'DDoS攻击'),('thirdreport', u'第三方报告'), ('exploitburst', u'新漏洞爆发'), ('misoperation ', u'操作不当')])
    level = SelectField(u'事件等级', choices=[('high', u'高危'), ('middle', u'中危'), ('low', u'低危')])

