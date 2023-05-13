from typing import Any
from django.contrib import admin

# Register your models here.
admin.site.site_header = "保险单据智能处理系统"  # 设置header
admin.site.site_title = "保险单据智能处理系统"  # 设置title
admin.site.index_title = "保险单据智能处理系统"
from django.utils.html import format_html
from .models import InsuranceDocument, SystemLog, InsuranceDocumentType
from .utils import kie_predict, kie_post_process
import json
from django_json_widget.widgets import JSONEditorWidget
from django.db import models
from import_export.admin import ImportExportModelAdmin
from fuzzywuzzy import fuzz

# 自定义字段展示
class InsuranceDocumentAdmin(ImportExportModelAdmin):
    # 定制展示字段
    list_display = (
        "upload_time",
        "status",
        "user",
        "document_type",
        "document_file_tag",
        "kie_result_img_tag",
        "kie_result_num",
        "kie_time_tag",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    # 不展示字段
    exclude = (
        "kie_result",
        "kie_result_img",
        "table_result",
        "table_result_img",
        "document_file_tag",
        "kie_result_img_tag",
        "kie_result_num",
    )

    # 只读字段
    readonly_fields = [
        "img_tag",
        # "kie_result_img_tag",
        # "document_file_tag",
        "user",
        "kie_time",
        "upload_time",
        "kie_result_num",
        "kie_time_tag",
    ]

    # 排序字段
    admin_order_field = ("kie_time_tag", "kie_result_num", "upload_time")

    # 定制可编辑字段
    # list_editable = (
    #     "document_type",
    #     "document_file",
    #     "insured_name",
    #     "insured_id_number",
    #     "beneficiary_name",
    #     "beneficiary_id_number",
    #     "insurance_amount",
    # )
    # 可以根据被保险人姓名, 受益人姓名进行搜索
    search_fields = ["insured_name", "beneficiary_name"]
    # 可以根据保单状态, 保单类型进行过滤
    list_filter = ("status", "document_type")
    # 设置每一页显示多少条记录
    list_per_page = 3

    # 自定义按钮
    actions = ["re_kie"]

    def re_kie(self, request, queryset):
        for insurance_document in queryset:
            # 进行关键信息抽取
            kie_res, kie_path, kie_time = kie_predict(
                insurance_document.document_file.path
            )
            kie_info = kie_post_process(kie_res)
            # 更新数据库
            insurance_document.kie_time = kie_time
            insurance_document.kie_result = kie_res
            insurance_document.kie_information = kie_info
            insurance_document.kie_result_num = len(kie_info)
            insurance_document.kie_result_img = kie_path.split("media/")[1]
            insurance_document.status = "分析完成"
            # 在kie_info字典中, 找包含保险人这个字段
            if str(insurance_document.document_type) in ("保单", "车险保单"):
                for key, value in kie_info.items():
                    if fuzz.ratio("被保险人", key) > 80:
                        insurance_document.insured_name = value
                    if fuzz.ratio("受益人姓名", key) > 80:
                        insurance_document.beneficiary_name = value
                    if fuzz.ratio("保险金额", key) > 80:
                        insurance_document.insurance_amount = value
                    if fuzz.ratio("被保险人身份证", key) > 80:
                        insurance_document.insured_id_number = value
                    if fuzz.ratio("受益人身份", key) > 80:
                        insurance_document.beneficiary_id_number = value
            insurance_document.save()
        pass

    # 显示的文本，与django admin一致
    re_kie.short_description = "重新抽取关键信息"
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    re_kie.type = "primary"

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        # 设置自己为默认用户
        if not change:
            obj.user = request.user
        # 先把图片存起来
        super().save_model(request, obj, form, change)
        # 进行关键信息抽取
        kie_res, kie_path, kie_time = kie_predict(obj.document_file.path)
        kie_info = kie_post_process(kie_res)
        # 更新数据库
        obj.kie_time = kie_time
        obj.kie_result = kie_res
        obj.kie_information = kie_info
        obj.kie_result_num = len(kie_info)
        obj.kie_result_img = kie_path.split("media/")[1]
        obj.status = "分析完成"
        # 在kie_info字典中, 找包含保险人这个字段
        if str(obj.document_type) in ("保单", "车险保单"):
            for key, value in kie_info.items():
                if fuzz.ratio("被保险人", key) > 80:
                    obj.insured_name = value
                if fuzz.ratio("受益人姓名", key) > 80:
                    obj.beneficiary_name = value
                if fuzz.ratio("保险金额", key) > 80:
                    obj.insurance_amount = value
                if fuzz.ratio("被保险人身份证", key) > 80:
                    obj.insured_id_number = value
                if fuzz.ratio("受益人身份", key) > 80:
                    obj.beneficiary_id_number = value
        return obj.save()


class InsuranceDocumentTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )


admin.site.register(InsuranceDocument, InsuranceDocumentAdmin)
admin.site.register(SystemLog)
admin.site.register(InsuranceDocumentType, InsuranceDocumentTypeAdmin)
