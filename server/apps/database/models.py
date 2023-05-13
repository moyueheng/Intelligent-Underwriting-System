from django.db import models
from users.models import User

# Create your models here.
from django.utils.safestring import mark_safe

from django.db import models
from os.path import join as pjoin

# from django.settings import BASE_DIR
from django.conf import settings


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
        verbose_name = "单据类型"

    def __str__(self) -> str:
        return self.name


class InsuranceDocument(models.Model):
    """保单模型类"""

    # 一个用户可以有多个保单
    # 默认选择我现在登陆的用户
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="用户",
        help_text="不用选择, 默认为当前登陆用户",
        null=True,
        blank=True,
    )
    document_type = models.ForeignKey(
        InsuranceDocumentType,
        on_delete=models.CASCADE,
        verbose_name="单据类型",
        help_text="必须选择类型",
    )

    STATUS = (
        ("未分析", "未分析"),
        ("分析中", "分析中"),
        ("分析完成", "分析完成"),
        ("分析失败", "分析失败"),
    )
    # 保单文件上传到media/documents/年/月/日/目录下, 必须上传文件, 保单文件名唯一
    document_file = models.ImageField(
        upload_to="documents/%Y/%m/%d/", verbose_name="单据文件", help_text="单据文件, 必须上传文件"
    )
    kie_time = models.FloatField(verbose_name="关键信息抽取时间", help_text="单位为秒", default=0.0)

    def kie_time_tag(self):
        return "{:.2f} s".format(self.kie_time)
    
    kie_time_tag.short_description = "关键信息抽取时间"

    upload_time = models.DateTimeField(
        auto_now_add=True, verbose_name="上传时间", help_text="上传时间"
    )

    # 更新时间
    update_time = models.DateTimeField(
        auto_now=True, verbose_name="更新时间", help_text="更新时间", null=True, blank=True
    )

    # 保单状态: 未分析, 分析中, 分析完成, 分析失败, 可选的
    status = models.CharField(
        max_length=8,
        verbose_name="抽取状态",
        choices=STATUS,
        help_text="抽取状态",
        default="未分析",
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

    # 在详细后台显示图片
    def img_tag(self):
        """
        <div style="display: flex; justify-content: space-around; border: 2px solid black; padding: 20px;">
            <img src="image1.jpg" alt="Image 1" width="400" style="border: 2px solid red;">
            <img src="image2.jpg" alt="Image 2" width="400" style="border: 2px solid red;">
        </div>
        """
        html_str = """<h2>提示:
            <span style="color:red">红色框为key</span>, 
            <span style="color:blue">蓝色框为value</span>, 
            <span style="color:green">绿色线为key和value的对应</span>
            </h2>
        <div style="display: flex; justify-content: space-around;  padding: 5px;">"""
        if self.document_file:
            html_str += '<img src="{}" style="width: 100%; max-width: 600px; border: 2px solid black;" />'.format(
                self.document_file.url
            )
        if self.kie_result_img:
            html_str += '<img src="{}" style="width: 100%; max-width: 600px;border: 2px solid black;" />'.format(
                self.kie_result_img.url
            )
        html_str += "</div>"
        return mark_safe(html_str)

    img_tag.short_description = "大图对比"

    def document_file_tag(self):
        if self.document_file:
            return mark_safe(
                '<img src="{}" width="300" height="300" />'.format(
                    self.document_file.url
                )
            )
        return "未上传单据文件"

    document_file_tag.short_description = "原始图片文件"

    def kie_result_img_tag(self):
        if self.kie_result_img:
            return mark_safe(
                '<img src="{}" width="300" height="300" />'.format(
                    self.kie_result_img.url
                )
            )
        return "未识别成功"

    kie_result_img_tag.short_description = "关键信息抽取图片文件"

    # 完整结果
    kie_result = models.JSONField(
        verbose_name="关键信息检测完整识别结果", help_text="以json形式展示", null=True, blank=True
    )
    # 后处理分析结果
    kie_information = models.JSONField(
        verbose_name="关键信息检测完整识别结果",
        help_text="后处理后分析结果",
        default=dict,
        null=True,
        blank=True,
    )
    # 关键信息抽取结果
    kie_result_img = models.ImageField(
        verbose_name="关键信息抽取可视化结果", help_text="以图片形式展示", null=True, blank=True
    )
    # 关键信息抽取识别数量
    kie_result_num = models.IntegerField(
        verbose_name="关键信息抽取识别数量",
        help_text="关键信息抽取识别数量",
        default=0,
        null=True,
        blank=True,
    )
    # 表格识别结果
    table_result = models.JSONField(
        verbose_name="表格识别结果", help_text="表格识别结果", default=dict, null=True, blank=True
    )
    # 表格识别可视化结果
    table_result_img = models.ImageField(
        verbose_name="表格识别可视化结果", help_text="以图片形式展示", null=True, blank=True
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


