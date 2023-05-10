from django.db import models
from users.models import User

# Create your models here.

from django.db import models
from os.path import join as pjoin
from django.db.models.signals import post_save
from django.dispatch import receiver
import sys

sys.path.append(
    "/root/BS/Intelligent-Underwriting-System/server/apps/database/PaddleOCR-release-2.6"
)
sys.path.append(
    "/root/BS/Intelligent-Underwriting-System/server/apps/database/PaddleOCR-release-2.6/ppstructure/kie"
)
from ppstructure.kie.predict_kie_token_ser_re import run

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
    document_file = models.ImageField(
        upload_to="documents/%Y/%m/%d/", verbose_name="保单文件", help_text="保单文件"
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
            "上传时间: "
            + self.upload_time.strftime("%Y-%m-%d %H:%M:%S")
            + ", 状态: "
            + self.status
        )


class KeyInformation(models.Model):
    """关键信息模型类"""

    # 一个保单可以有多个关键信息分析结果
    insurance_document_id = models.ForeignKey(
        InsuranceDocument, on_delete=models.CASCADE, verbose_name="保单", help_text="保单"
    )
    insured_name = models.CharField(
        max_length=50, verbose_name="被保险人姓名", help_text="被保险人姓名", default="未知"
    )
    insured_id_number = models.CharField(
        max_length=50, verbose_name="被保险人身份证号", help_text="被保险人身份证号", default="未知"
    )
    beneficiary_name = models.CharField(
        max_length=50, verbose_name="受益人姓名", help_text="受益人姓名", default="未知"
    )
    beneficiary_id_number = models.CharField(
        max_length=50, verbose_name="受益人身份证号", help_text="受益人身份证号", default="未知"
    )
    insurance_amount = models.FloatField(
        verbose_name="保险金额", help_text="保险金额", default=0
    )

    # 完整结果
    result = models.JSONField(verbose_name="分析结果", help_text="分析结果")
    # 关键信息
    key_information = models.JSONField(
        verbose_name="关键信息", help_text="关键信息", default=dict
    )
    # 可视化结果
    result_img = models.ImageField(verbose_name="可视化识别结果", help_text="可视化结果")

    class Meta:
        db_table = "key_information"
        verbose_name = "关键信息"


# 监听InsuranceDocument模型创建
@receiver(post_save, sender=InsuranceDocument)
def create_insurance_document(sender, instance, created, **kwargs):
    # 如果是新创建的保单, 则创建关键信息模型
    if created:
        # 调用模型进行检测
        # media_root = '/root/BS/Intelligent-Underwriting-System/server/media'
        re_res, img_save_path = run(
            instance.document_file.path, instance.document_file.path.split(".")[0]
        )
        # 将返回的结果保存到KeyInformation模型中
        result_img = img_save_path.replace(
            "/root/BS/Intelligent-Underwriting-System/server/media", ""
        )
        instance.status = "分析完成"
        instance.save()
        # 对re_res进行处理
        def get_key_information(result):
            key_information = []
            for item in result:
                temp_data = {}
                for sub_item in item:
                    if sub_item["pred"] == "QUESTION":
                        temp_data["question"] = sub_item["transcription"]
                    elif sub_item["pred"] == "ANSWER":
                        temp_data["answer"] = sub_item["transcription"]
                key_information.append(temp_data)
            return key_information
        
        key_information = get_key_information(re_res)

        KeyInformation.objects.create(
            insurance_document_id=instance,
            key_information=key_information,
            result=re_res,
            result_img=result_img,
        )


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


if __name__ == "__main__":

    re_res, img_save_path = run(
        "/root/BS/Intelligent-Underwriting-System/server/media/documents/2023/05/09/机动车交通事故责任强制保险单.jpg",
        "/root/BS/Intelligent-Underwriting-System/server/media/documents/2023/05/09/机动车交通事故责任强制保险单",
    )
    # 将返回的结果保存到KeyInformation模型中
    # KeyInformation.objects.create(insurance_document_id=instance,result = re_res, result_img = img_save_path, **kwargs)
