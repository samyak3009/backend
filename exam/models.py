from django import db
from django.db import models
from jsonfield import JSONField

class StudentDetails(models.Model):
    name = models.CharField(db_column='name',max_length=250)
    course = models.CharField(db_column='course',max_length=250)
    date_of_birth = models.DateField(db_column='date_of_birth',blank=True,null=True)
    email = models.CharField(db_column='email',max_length=250)
    mobile = models.CharField(db_column='mobile',max_length=250)
    username = models.CharField(db_column='username',max_length=250)
    password = models.CharField(db_column='password',max_length=250)
    class Meta:
        managed = True
        db_table = 'StudentDetails'

class ExamDetail(models.Model):
    course = models.CharField(db_column='course',max_length=250)
    subject = models.CharField(db_column='subject',max_length=250)
    exam_title = models.CharField(db_column='exam_title',max_length=250)
    date_of_exam = models.CharField(db_column='date_of_exam',max_length=250)
    start_time = models.CharField(db_column='start_time',max_length=250)
    end_time = models.CharField(db_column='end_time',max_length=250)
    status = models.CharField(max_length=20, default='INSERT')
    class Meta:
        managed = True
        db_table = 'ExamDetail'

class ExamAttribute(models.Model):
    form_id = models.ForeignKey(ExamDetail, related_name='ExamAttributes_id', null=True, on_delete=models.SET_NULL, db_column='form_id')
    max_marks = models.CharField(db_column='max_marks',max_length=250,null=True)
    element_id = models.IntegerField(db_column='Element_Id')
    attribute = JSONField()
    class Meta:
        managed = True
        db_table = 'ExamAttribute'

class ExamSession(models.Model):
    student_id = models.ForeignKey(StudentDetails,related_name='ExamSession',null=True, on_delete=models.SET_NULL, db_column='student_id')
    form_id = models.ForeignKey(ExamDetail,related_name='Exam_form',null=True, on_delete=models.SET_NULL, db_column='form_id')
    form_status = models.IntegerField(db_column='form_status',default=0)
    class Meta:
        managed = True
        db_table = 'ExamSession'

class ExamAnswer(models.Model):
    ques_id = models.ForeignKey(ExamAttribute,related_name='Element_que_Id',null=True,on_delete=models.SET_NULL,db_column='Ques_id')
    ans_id = models.ForeignKey(ExamSession,related_name='ExamSession_id',null=True,on_delete=models.SET_NULL,db_column='ans_id')
    ans_attribute = JSONField()
    class Meta:
        managed = True
        db_table = 'ExamAnswer'


