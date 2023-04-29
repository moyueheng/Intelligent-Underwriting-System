from django.db import models
from users.models import User

# Create your models here.

from django.db import models

class InsuranceDocument(models.Model):
    # 一个用户可以有多个保单
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    document_number = models.CharField(max_length=255, verbose_name='保单号')
    document_type = models.CharField(max_length=255, verbose_name='保单类型')
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    status = models.CharField(max_length=255, verbose_name='状态')

    class Meta:
        db_table = 'insurance_documents'



class DocumentAnalysisResult(models.Model):
    # 一个保单可以有多个分析结果
    insurance_document = models.ForeignKey(InsuranceDocument, on_delete=models.CASCADE, verbose_name='保单')
    text_detection_result = models.JSONField(verbose_name='文本检测结果')
    text_recognition_result = models.JSONField(verbose_name='文本识别结果')
    layout_analysis_result = models.JSONField(verbose_name='版面分析结果')

    class Meta:
        db_table = 'document_analysis_results'



class KeyInformation(models.Model):
    # 一个保单可以有多个关键信息
    insurance_document_id = models.ForeignKey(InsuranceDocument, on_delete=models.CASCADE, verbose_name='保单')
    insured_name = models.CharField(max_length=50, verbose_name='被保险人姓名')
    insured_id_number = models.CharField(max_length=50, verbose_name='被保险人身份证号')
    beneficiary_name = models.CharField(max_length=50, verbose_name='受益人姓名')
    beneficiary_id_number = models.CharField(max_length=50, verbose_name='受益人身份证号')
    insurance_amount = models.FloatField(verbose_name='保险金额')

    class Meta:
        db_table = 'key_information'


class SystemLog(models.Model):
    # 一个用户可以有多个操作日志
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    operation_type = models.CharField(max_length=255, verbose_name='操作类型')
    operation_time = models.DateTimeField(verbose_name='操作时间')
    operation_detail = models.JSONField(verbose_name='操作详情')
    ip_address = models.CharField(max_length=255, verbose_name='IP地址')

    class Meta:
        db_table = 'system_logs'





