import sys
sys.path.append('/root/BS/Intelligent-Underwriting-System/server/apps/database/PaddleOCR-release-2.6')
sys.path.append('/root/BS/Intelligent-Underwriting-System/server/apps/database/PaddleOCR-release-2.6/ppstructure/kie')

from ppstructure.kie.predict_kie_token_ser_re import run

re_res, img_save_path = run("/root/BS/Intelligent-Underwriting-System/server/media/documents/2023/05/09/机动车交通事故责任强制保险单.jpg", "/root/BS/Intelligent-Underwriting-System/server/media/documents/2023/05/09")
print(re_res)
print(img_save_path)