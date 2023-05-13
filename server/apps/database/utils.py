DEBUG = True
import sys
from os.path import join as pjoin
from django.conf import settings

if DEBUG:
    sys.path.append(
        pjoin(
            "/root/BS/Intelligent-Underwriting-System/server",
            "apps/database/PaddleOCR-release-2.6",
        )
    )

    sys.path.append(
        pjoin(
            "/root/BS/Intelligent-Underwriting-System/server",
            "apps/database/PaddleOCR-release-2.6/ppstructure/kie",
        )
    )
else:
    sys.path.append(
        pjoin(settings.BASE_DIR.parent, "apps/database/PaddleOCR-release-2.6")
    )

    sys.path.append(
        pjoin(
            settings.BASE_DIR.parent,
            "/apps/database/PaddleOCR-release-2.6/ppstructure/kie",
        )
    )
from ppstructure.kie.predict_kie_token_ser_re import kie_run

# 关键信息抽取
def kie_predict(img_path):
    out_put_dir = img_path.split(".")[0]
    return kie_run(img_path, out_put_dir)

# 关键信息进行后处理, 变成前端方便处理的格式
def kie_post_process(kie_result):
    kie_information = {}
    for question, answer in kie_result:
        if kie_information.get(question['transcription'], None):
            kie_information[question['transcription']] += answer['transcription']
        else:
            kie_information[question['transcription']] = answer['transcription']
    return kie_information

# 表格识别
def table_predict(img_path):
    pass


if __name__ == "__main__":
    kie_predict("/root/BS/Intelligent-Underwriting-System/server/media/documents/2023/05/12/发票.jpg")
    pass