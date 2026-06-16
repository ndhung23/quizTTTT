import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Attach SQLAlchemy to the Flask app and create tables."""
    db.init_app(app)
    with app.app_context():
        from app.models import user, student, session, quiz_option, quiz_step  # noqa: F401 – register models
        db.create_all()
        try:
            db.session.execute(db.text("ALTER TABLE quiz_sessions ADD COLUMN quiz_type VARCHAR(20) DEFAULT 'option1'"))
            db.session.commit()
            print("Successfully added quiz_type column to quiz_sessions")
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(db.text("ALTER TABLE quiz_sessions ADD COLUMN user_id INTEGER"))
            db.session.commit()
            print("Successfully added user_id column to quiz_sessions")
        except Exception:
            db.session.rollback()
        _seed_users()
        _seed_quiz_options()


def _seed_users():
    """Insert default users or update passwords."""
    from app.models.user import User
    try:
        users_to_check = [
            {"username": "admin", "password": "hdvn@dens0", "role": "admin"},
            {"username": "hv90122", "password": "hdvn@dens0", "role": "teacher"},
            {"username": "hv10921", "password": "hdvn@dens0", "role": "teacher"},
        ]
        for u_data in users_to_check:
            user = User.query.filter_by(username=u_data["username"]).first()
            if not user:
                user = User(username=u_data["username"], password=u_data["password"], role=u_data["role"])
                db.session.add(user)
            else:
                user.password = u_data["password"]
                user.role = u_data["role"]
        db.session.commit()
        print("Synchronized default users and updated passwords to 'hdvn@dens0'")
    except Exception as e:
        db.session.rollback()
        print(f"Seed/update warning: {e}")


def _seed_quiz_options():
    """Seed initial Option 1 quiz and steps."""
    from app.models.quiz_option import QuizOption
    from app.models.quiz_step import QuizStep
    try:
        option1 = QuizOption.query.filter_by(code="option1").first()
        if not option1:
            option1 = QuizOption(title="Kiểm tra thao tác đúc", code="option1", is_custom=False)
            db.session.add(option1)
            db.session.commit()

            left_texts = [
                "Trước khi vào thao tác cần tuân thủ đeo đồ bảo hộ: Mũ, kính, gang tay, xỏ tay, giày bảo hộ",
                "Đặt Terminal SA lên bề mặt khuôn trong",
                "Lấy sản phẩm từ khuôn đặt vào băng tải",
                "Lấy terminal S/A set vào khuôn trong",
                "Lấy terminal ngắn từ khay",
                "Set terminal ngắn vào khuôn phía ngoài",
                "Lấy terminal dài từ khay",
                "Set terminal dài vào khuôn phía ngoài",
                "—",
                "Lấy jig set Bush từ vị trí để jig \n(Áp dụng máy đúc số 12)",
                "Đặt jig set bush\n lên khuôn",
                "Hai tay bóp mạnh vị trí tay cầm để set 6 bush vào vị trí cố định",
                "—",
                "—",
                "Chỉnh jig",
                "Hai tay bóp mạnh vị trí tay cầm để set 6 bush vào \nvị trí cố định ",
                "—",
                "Nhấc jig set bush đặt\n vào vị trí để jig\n(Áp dụng máy đúc số 12)",
                "—",
                "Các ngón tay giữ cố \nđịnh các terminal trên khuôn.",
                "Bóp vào dâu slide sau đó từ từ set conector khớp vào các \nchân terminal",
                "Kiểm tra các lỗ của terminal có khớp với chân pin \nkhông?",
                "—"
            ]

            right_texts = [
                "—",
                "Đặt Terminal SA lên bề mặt khuôn ngoài",
                "Lấy sản phẩm từ khuôn đặt vào băng tải",
                "Lấy terminal S/A set vào khuôn ngoài",
                "Lấy terminal ngắn từ khay",
                "Set terminal ngắn vào khuôn trong",
                "Lấy terminal dài từ khay",
                "Set terminal dài vào khuôn trong",
                "Lấy súng khí làm sạch khuôn",
                "Lấy jig set Bush từ vị trí để jig \n(Áp dụng máy đúc số 3)",
                "Chỉnh jig",
                "Hai tay bóp mạnh vị trí tay cầm để set 6 bush vào vị trí cố định",
                "Ấn vào vị trí trung tâm của jig",
                "Nhấc jig set bush xoay 180°",
                "Đặt jig set bush vào nửa khuôn trong.",
                "Hai tay bóp mạnh vị trí tay cầm để set 6 bush vào ",
                "Ấn vào vị trí trung tâm của jig",
                "Nhấc jig set bush đặt\n vào vị trí để jig\n(Áp dụng máy đúc số 3)",
                "Xác nhận đủ bush,bush không bị kênh",
                "Bóp vào dâu slide sau đó từ từ set conector  khớp vào các chân terminal",
                "Các ngón tay giữ cố định\n các terminal trên khuôn",
                "Kiểm tra các lỗ của terminal có khớp với chân pin \nkhông?",
                "Gạt công tắc"
            ]

            note_texts = [
                "Đảm bảo an toàn khi thao tác:\n1. Mũ đội chùm kín tóc\n2.Đeo kính không được trễ xuống mũi\n3.Gang tay, xỏ tay không rách thủng, đeo xỏ tay phải qua khủy tay, không để lộ cánh tay\n4. Giày bảo hộ thắt nút buộc dây chặt chẽ",
                "1.Khi đèn xanh sáng mới được vào thao tác\nKhông làm va linh kiện vào các vị trí trên khuôn",
                "1.Nhấc sản phẩm trước khi chân pin hạ xuống hết , nhấc vuông góc.\n2. Đặt 2 sản phẩm cùng chiều, không xếp chồng lên nhau và phần conector hướng về phía người thao tác đúc.",
                "1. Lỗ trên terminal khớp với chân pin trên khuôn.\n2. Ngón tay cái ấn các lỗ pin từ phía IC ra tới đầu các chân terminal.",
                "Terminal không bị cong.",
                "Xác nhận lỗ trên terminal khớp với chân pin trên khuôn.",
                "Terminal không bị cong.",
                "Xác nhận lỗ trên terminal khớp với chân pin trên khuôn.",
                "1. Cầm vào vị trí tay cầm kéo súng khí sát bề mặt khuôn.\n2. Xì khí đến khi hệ thống làm sạch khuôn tự ngắt    ",
                "Cầm chắc ở phần trung tâm của jig, tránh làm rơi.",
                "1. Hướng nhãn màu \ncam về phía người thao tác\n2.Chân jig khớp with các lỗ \ntrên khuôn \n3.Nhấc jig, chân jig cao hơn đầu conector",
                "Bóp hết cỡ, dứt khoát, đồng thời cả hai tay.",
                "Dùng lòng bàn tay phải ấn hết cỡ đến khi có tiếng kêu cạch",
                "1.Nhấc jig, chân jig cao hơn đầu conector\n2.Hướng nhãn màu cam về phía đối diện người thao tác",
                "\nChân jig khớp với lỗ trên khuôn ",
                "Bóp tay cầm hết cỡ, dứt khoát, đồng thời cả hai tay.",
                "Dùng lòng bàn tay phải ấn hết cỡ đến khi có tiếng kêu cạch",
                "Cầm chắc chắn, xoay jig 180̊ để hướng nhãn màu cam về phía gần người thao tác",
                "1.Chỉ tay xác nhận theo chiều kim đồng hồ, mắt nhìn theo tay.\n2. Bắt đầu từ vị trí bush  bên trái gần  NTT nhất \n",
                "1.Tay phải bóp vào vị trí của Slide\n trên conector.\n2.Các chân terminal nằm trên 1 mặt phẳng, khớp với chân pin  trên khuôn.",
                "1.Tay trái bóp vào vị trí của Slide\n trên conector\n2.Các chân terminal nằm trên 2 mặt phẳng, khớp với chân pin\n trên khuôn.",
                "Dùng các ngón tay ấn (không miết) các chân terminal khớp với chân pin.",
                "1. Vừa xoay người vừa gạt công tắc.\n2. Người không đứng trong khu vực cảm biến"
            ]

            reason_texts = [
                "1. Tránh dị vật tóc rơi vào sản phẩm.\n2.Dị vật bắn vào mắt\n3. Chạm vào vật có nhiệt độ cao gây bỏng tay.\n4.Vấp ngã khi thao tác",
                "NG linh kiện",
                "1. Máy báo lỗi , mất an toàn\n2&3 .Sản phẩm bị xước",
                "Tạo phế phẩm : Lộ terminal",
                "Tạo phế phẩm:\nCong terminal không set vào khuôn được",
                "Tạo phế phẩm:\nNhựa phủ moter terminal, Terminal bị lộ",
                "Tạo phế phẩm:\nCong terminal không set vào khuôn được",
                "Tạo phế phẩm:\nnhựa phủ moter terminal, Terminal bị lộ",
                "1. Khí làm sạch khuôn không thổi ra\n2. Không làm sạch hết dị vật\n",
                "1. Hỏng jig.\n2. Sứt mẻ khuôn.\n3. Rơi jig vào chân gây bị thương.",
                "1. Bốn  Bush không vào đúng vị trí\n2. Mẻ khuôn\n3. Tạo lỗi xước miệng conector và lòng sản phẩm.",
                "1.Bush không rơi xuống pin.\n2.Tạo phế phẩm thiếu bush.",
                "Không ấn hết bush \n=> Bush bị kênh,tạo lỗi nhựa tràn bush ,bush biến dạng",
                "1. Tạo lỗi xước miệng conector và lòng sản phẩm.\n2. Bốn  Bush không vào đúng vị trí",
                "Bốn  Bush không vào đúng vị trí\n",
                "1.Bush không rơi xuống pin.\n2.Tạo phế phẩm thiếu bush.",
                "Không ấn hết bush \n=> Bush bị kênh,tạo lỗi nhựa tràn bush ,bush biến dạng",
                "1. Hỏng jig.\n2. Sứt mẻ khuôn.\n3. Rơi jig vào chân gây bị thương.",
                "1.Tạo phế phẩm: thiếu bush, nhựa tràn bush,\n2.Sai quy định",
                "1.Không nhả được Slide\n2.Tạo phế phẩm: lộ terminal, terminal cong.",
                "1.Không nhả được Slide\n3.Tạo phế phẩm: lộ terminal, terminal cong",
                "Tạo phế phẩm: lộ \nterminal, dị vật khác kim loại (từ găng tay)",
                "Máy báo lỗi"
            ]

            for i in range(23):
                step = QuizStep(
                    option_id=option1.id,
                    step_num=i + 1,
                    image_url=f"/images/{i + 1}.png",
                    left_text=left_texts[i],
                    right_text=right_texts[i],
                    note_text=note_texts[i],
                    reason_text=reason_texts[i]
                )
                db.session.add(step)
            db.session.commit()
            print("Seeded Option 1 successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Option seed warning: {e}")


