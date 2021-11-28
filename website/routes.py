import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Blueprint ,render_template, request, redirect, url_for
from website import app, db, utils
from website.models import BenhNhan, DanhSachKham, TaiKhoan, PhieuKham, ToaThuoc, Thuoc, chitiettoathuoc, HoaDon

yta = Blueprint('yta', __name__)
user = Blueprint('user', __name__)
bacsi = Blueprint('bacsi', __name__)
admin = Blueprint('admin', __name__)

@user.route('/')
def home():
    return render_template('home.html')


# Xử lí các trang
#--------------------NGƯỜI DÙNG---------------------


#--------------------Y TÁ---------------------
@yta.route('/yta/home')
def yta_home():
    return render_template('yta.html')


#--------------------BÁC SĨ--------------------
#home
@bacsi.route('/home')
def home():
    return render_template('bacSi.html')


#Xem tất cả bệnh nhân
@bacsi.route('/danhsachkhambacsi')
def bacsi_danhsachkhambacsi():
    danhsachkham = utils.get_danhsachchuakham()
    return render_template('danhsachkhambacsi.html', danhsachkham=danhsachkham)
#Danh sách bệnh nhân
@bacsi.route('/danhsachbenhnhan')
def bacsi_danhsachbenhnhan():
    danhsach = utils.get_allbenhnhan()
    return render_template('danhsachbenhnhan.html', danhsach=danhsach)

#thêm vào bệnh nhân 
@bacsi.route('/themdanhsachkhambacsi', methods=['GET', 'POST'])
def bacsi_thembenhnhan():
    cmnd = request.args.get('cmnd', 123, type = str)
    benhnhan = utils.get_benhnhanbycmnd(cmnd)
    benhnhanmoi = utils.get_danhsachkhambycmnd(cmnd)
    print(cmnd)
    print(benhnhanmoi)
    if benhnhan == None:
        hoten = benhnhanmoi.hoten
        namsinh = benhnhanmoi.namsinh
        gioitinh = benhnhanmoi.gioitinh
        diachi = benhnhanmoi.diachi
        cmnd = benhnhanmoi.cmnd
        sdt = benhnhanmoi.sdt
        thembenhnhan = BenhNhan(hoten = hoten,
                                gioitinh = gioitinh,
                                namsinh = namsinh,
                                diachi = diachi,
                                cmnd = cmnd,
                                sdt = sdt)
        try:
            db.session.add(thembenhnhan)
            benhnhanmoi.trangthai = 1
            db.session.commit()
            print("Them thanh cong")
            return redirect(url_for('bacsi.bacsi_phieuKhamBenh',cmnd = cmnd))
        except:
            print("Them that bai")
    else:
        benhnhanmoi.trangthai = 1
        db.session.commit()
        
    return render_template('phieuKhamBenh.html')

@bacsi.route('/xoadanhsachkhambacsi/<int:id>', methods=['GET','POST'])
def bacsi_xoadanhsachkhambacsi(id):
    id = str(id)
    danhsachkham = DanhSachKham.query.filter(DanhSachKham.mads == id).first()
    try:
        db.session.delete(danhsachkham)
        db.session.commit()
        print("xoa thanh cong")
        return redirect(url_for("bacsi.bacsi_danhsachkhambacsi"))
    except:
        print("xoa that bai")
    return redirect(url_for("bacsi.bacsi_danhsachkhambacsi"))
#Xóa bệnh nhân trong bảng bệnh nhân
@bacsi.route('/xoadanhsachbenhnhan/<int:id>', methods=['GET', 'POST'])
def bacsi_xoadanhsachbenhnhan(id):
    id = str(id)
    benhnhan = BenhNhan.query.filter(BenhNhan.mabn == id).first()
    print(benhnhan)
    try:
        db.session.delete(benhnhan)
        db.session.commit()
        print("Xoa thanh cong")
        return redirect(url_for("bacsi.bacsi_danhsachbenhnhan"))
    except:
        print("Xoa that bai")

    return redirect(url_for("bacsi.bacsi_danhsachbenhnhan"))


@bacsi.route('/phieuKhamBenh', methods=['GET','POST'])
def bacsi_phieuKhamBenh():
    cmnd = request.args.get('cmnd', 123, type = str)
    print(cmnd)
    benhnhan = utils.get_benhnhanbycmnd(cmnd)
    ngaykham = utils.today
    trieuchung = request.form.get('trieuchung')
    loaibenh = request.form.get('loaibenh')
    tienkham = request.form.get('tienkham')
    phieukham = PhieuKham(trieuchung = trieuchung,
                          ngaykham = ngaykham,
                          loaibenh = loaibenh,
                          tienkham = tienkham,
                          o_benhnhan = benhnhan
                          )
    try:
        db.session.add(phieukham)
        db.commit()
        return redirect(url_for('bacsi.bacsi_phieuKhamBenh', mapk = phieukham.mapk))
    except:
        print("them that bai")

    return render_template('phieuKhamBenh.html', mabn = benhnhan.mabn , ngaykham = ngaykham, mapk = phieukham.mapk)

@bacsi.route('/xuathoadon')
def bacsi_xuathoadon():

    return render_template('xuathoadon.html')




@bacsi.route('/lichsubenhnhan')
def bacsi_lichsubenhnhan():
    return render_template('lichsubenhnhan.html')
#--------------------ADMIN---------------------


def create_app():
    app.register_blueprint(yta, url_prefix='/yta')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(bacsi, url_prefix='/bacsi')
    app.register_blueprint(user, url_prefix='/')
    return app