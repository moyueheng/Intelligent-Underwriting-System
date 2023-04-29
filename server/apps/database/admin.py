from django.contrib import admin

# Register your models here.
admin.site.site_header = "保险单据智能处理系统"  # 设置header
admin.site.site_title = "保险单据智能处理系统"  # 设置title
admin.site.index_title = "保险单据智能处理系统"


from .models import InsuranceDocument, DocumentAnalysisResult, KeyInformation, SystemLog, InsuranceDocumentType

admin.site.register(InsuranceDocument)
admin.site.register(DocumentAnalysisResult)
admin.site.register(KeyInformation)
admin.site.register(SystemLog)
admin.site.register(InsuranceDocumentType)
