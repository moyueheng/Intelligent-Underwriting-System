from django.contrib import admin

# Register your models here.
admin.site.site_header = "保险单据智能处理系统"  # 设置header
admin.site.site_title = "保险单据智能处理系统"  # 设置title
admin.site.index_title = "保险单据智能处理系统"
from .forms import KeyInformationForm
from django.utils.html import format_html
from .models import InsuranceDocument, KeyInformation, SystemLog, InsuranceDocumentType

# 自定义字段展示
class InsuranceDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "upload_time",
        "status",
        "user",
        "document_type",
    )


class KeyInformationAdmin(admin.ModelAdmin):
    change_form_template = "admin/database/database/change_form.html"
    form = KeyInformationForm
    list_display = (
        "insurance_document_id",
        "result_img",
    )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        instance = KeyInformation.objects.get(pk=object_id)
        result = instance.result
        processed_data = self.process_result_data(result)
        extra_context["processed_data"] = processed_data
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

    def process_result_data(self, result):
        processed_data = []
        for item in result:
            temp_data = {}
            for sub_item in item:
                if sub_item["pred"] == "QUESTION":
                    temp_data["question"] = sub_item["transcription"]
                elif sub_item["pred"] == "ANSWER":
                    temp_data["answer"] = sub_item["transcription"]
            processed_data.append(temp_data)
        return processed_data


class InsuranceDocumentTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )


admin.site.register(InsuranceDocument, InsuranceDocumentAdmin)
admin.site.register(KeyInformation, KeyInformationAdmin)
admin.site.register(SystemLog)
admin.site.register(InsuranceDocumentType, InsuranceDocumentTypeAdmin)
