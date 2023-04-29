from tabnanny import verbose
from django.db import models
from users.models import User

# Create your models here.

from django.db import models


# 保险单据类型
class InsuranceDocumentType(models.Model):
    """保单类型模型类"""

    name = models.CharField(
        max_length=255, verbose_name="保单类型", help_text="保单类型", unique=True
    )
    description = models.CharField(
        max_length=255, verbose_name="保单类型描述", help_text="保单类型描述"
    )

    class Meta:
        db_table = "insurance_document_types"
        verbose_name = "保单类型"

    def __str__(self) -> str:
        return self.name


class InsuranceDocument(models.Model):
    """保单模型类"""

    # 一个用户可以有多个保单
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="用户", help_text="用户"
    )
    document_type = models.ForeignKey(
        InsuranceDocumentType,
        on_delete=models.CASCADE,
        verbose_name="保单类型",
        help_text="保单类型",
    )

    STATUS = (
        ("未分析", "未分析"),
        ("分析中", "分析中"),
        ("分析完成", "分析完成"),
        ("分析失败", "分析失败"),
    )
    # 保单文件上传到media/documents/年/月/日/目录下, 必须上传文件, 保单文件名唯一
    document_file = models.FileField(
        upload_to="documents/%Y/%m/%d/", verbose_name="保单文件", help_text="保单文件"
    )

    document_number = models.CharField(
        max_length=255, verbose_name="保单号", help_text="保单号", unique=True
    )
    upload_time = models.DateTimeField(
        auto_now_add=True, verbose_name="上传时间", help_text="上传时间"
    )
    # 保单状态: 未分析, 分析中, 分析完成, 分析失败, 可选的
    status = models.CharField(
        max_length=8,
        verbose_name="保单状态",
        choices=STATUS,
        help_text="保单状态",
        default="未分析",
    )

    class Meta:
        db_table = "insurance_documents"
        verbose_name = "保单"

    def __str__(self) -> str:
        return (
            "保单号: "
            + self.document_number
            + ", 上传时间: "
            + self.upload_time.strftime("%Y-%m-%d %H:%M:%S")
            + ", 状态: "
            + self.status
        )


class DocumentAnalysisResult(models.Model):
    """保单分析结果模型类"""

    # 一个保单可以有多个分析结果
    insurance_document = models.ForeignKey(
        InsuranceDocument, on_delete=models.CASCADE, verbose_name="保单", help_text="保单"
    )
    text_detection_result = models.JSONField(verbose_name="文本检测结果", help_text="文本检测结果")
    text_recognition_result = models.JSONField(
        verbose_name="文本识别结果", help_text="文本识别结果"
    )
    layout_analysis_result = models.JSONField(verbose_name="版面分析结果", help_text="版面分析结果")

    class Meta:
        db_table = "document_analysis_results"
        verbose_name = "保单分析结果"


class KeyInformation(models.Model):
    """关键信息模型类"""

    # 一个保单可以有多个关键信息
    insurance_document_id = models.ForeignKey(
        InsuranceDocument, on_delete=models.CASCADE, verbose_name="保单", help_text="保单"
    )
    insured_name = models.CharField(
        max_length=50, verbose_name="被保险人姓名", help_text="被保险人姓名"
    )
    insured_id_number = models.CharField(
        max_length=50, verbose_name="被保险人身份证号", help_text="被保险人身份证号"
    )
    beneficiary_name = models.CharField(
        max_length=50, verbose_name="受益人姓名", help_text="受益人姓名"
    )
    beneficiary_id_number = models.CharField(
        max_length=50, verbose_name="受益人身份证号", help_text="受益人身份证号"
    )
    insurance_amount = models.FloatField(verbose_name="保险金额", help_text="保险金额")

    class Meta:
        db_table = "key_information"
        verbose_name = "关键信息"


class SystemLog(models.Model):
    """系统日志模型类"""

    # 一个用户可以有多个操作日志
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="用户", help_text="用户"
    )
    operation_type = models.CharField(
        max_length=255, verbose_name="操作类型", help_text="操作类型"
    )
    operation_time = models.DateTimeField(verbose_name="操作时间", help_text="操作时间")
    operation_detail = models.JSONField(verbose_name="操作详情", help_text="操作详情")
    ip_address = models.CharField(max_length=255, verbose_name="IP地址", help_text="IP地址")

    class Meta:
        db_table = "system_logs"
        verbose_name = "系统日志"
