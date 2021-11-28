# Import các thư viện cần thiết
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from website.models import BenhNhan, DanhSachKham, TaiKhoan, PhieuKham, ToaThuoc, Thuoc, chitiettoathuoc, HoaDon
from website import db
from datetime import datetime, timedelta

# Lấy thời gian ngày hôm nay [ngày và giờ hiện tại]
today_str = datetime.today()
# Chuyển thời gian lấy được qua String
date_str = today_str.strftime("%Y-%m-%d")
# Chuyển thời gian từ String qua DateTime [ngày hiện tại, giờ 00:00:00]
today = today_str.strptime(date_str, "%Y-%m-%d")
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

# Xử lí các chức năng CRUD
#--------------------TÀI KHOẢN---------------------
def get_taikhoan():
    return TaiKhoan.query.all()

#--------------------DANH SÁCH KHÁM---------------------
def get_alldanhsachkham():
    return DanhSachKham.query.all()
def get_danhsachchuakham():
    return DanhSachKham.query.filter(DanhSachKham.trangthai==0).all()
def get_danhsachkhambycmnd(cmnd):
    benhnhanmoi = DanhSachKham.query.filter(DanhSachKham.cmnd == cmnd).first()
    return benhnhanmoi
def get_danhsachkhambyid(id):
    danhsachkham = DanhSachKham.query.filter(DanhSachKham.id == id).first()
    return danhsachkham
#--------------------BỆNH NHÂN---------------------
def get_benhnhanbycmnd(cmnd):
    benhnhan = BenhNhan.query.filter(BenhNhan.cmnd == cmnd).first()
    return benhnhan
def get_allbenhnhan():
    return BenhNhan.query.all()
def get_benhnhandau():
    return BenhNhan.query.get(1)
def get_benhnhanbymabn(mabn):
    benhnhan = BenhNhan.query.filter(BenhNhan.mabn == mabn).first()
    return benhnhan

#--------------------PHIẾU KHÁM--------------------
# def add_phieukham(ngaykham, trieuchung, loaibenh, tienkham):
#     benhnhan1 = BenhNhan.query.filter().first()
#     phieukham = PhieuKham(
#         ngaykham = ngaykham,
#         trieuchung = trieuchung,
#         loaibenh = loaibenh,
#         tienkham = tienkham,
#         o_benhnhan = benhnhan1
#     )
#     try:
#         db.session.add(phieukham)
#         db.session.commit()
#         return True
#     except Exception as ex:
#         print("RECEIPT ERROR: " + str(ex))

#--------------------TOA THUỐC---------------------

#----------------CHI TIẾT TOA THUỐC----------------

#---------------------THUỐC------------------------

#---------------------HOÁ ĐƠN----------------------

#-----------------DANH SÁCH KHÁM-------------------
# if __name__=="__main__":
#     print(get_benhnhanbymabn(1))

