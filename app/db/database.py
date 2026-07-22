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
            db.session.execute(db.text("ALTER TABLE quiz_sessions ADD COLUMN quiz_type VARCHAR(50) DEFAULT 'option1'"))
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
        try:
            db.session.execute(db.text("ALTER TABLE quiz_options ADD COLUMN quiz_format VARCHAR(20) DEFAULT 'option1'"))
            db.session.commit()
            print("Successfully added quiz_format column to quiz_options")
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(db.text("ALTER TABLE students ADD COLUMN tab_switch_count INTEGER DEFAULT 0"))
            db.session.commit()
            print("Successfully added tab_switch_count column to students")
        except Exception:
            db.session.rollback()
        _seed_users()
        _seed_quiz_options()

        # NFC normalization for legacy database records
        try:
            import unicodedata
            from app.models.quiz_option import QuizOption
            from app.models.session import QuizSession
            
            # Normalize QuizOption codes
            options = QuizOption.query.all()
            for opt in options:
                if opt.code:
                    norm = unicodedata.normalize('NFC', opt.code)
                    if norm != opt.code:
                        opt.code = norm
            
            # Normalize QuizSession quiz_types
            sessions = QuizSession.query.all()
            for sess in sessions:
                if sess.quiz_type:
                    # Repair corrupted 'c' or '\ufffdc' back to 'đúc'
                    if '\ufffd' in sess.quiz_type or '\xc4' in sess.quiz_type or sess.quiz_type.endswith('c') and len(sess.quiz_type) <= 3:
                        if sess.quiz_type.endswith('c'):
                            sess.quiz_type = 'đúc'
                    norm = unicodedata.normalize('NFC', sess.quiz_type)
                    if norm != sess.quiz_type:
                        sess.quiz_type = norm
                        
            db.session.commit()
            print("Successfully normalized existing DB tables to NFC and repaired legacy session records")
        except Exception as e:
            db.session.rollback()
            print(f"NFC Normalization warning: {e}")


def _seed_users():
    """Insert default users if they do not exist (do not overwrite existing passwords/roles)."""
    from app.models.user import User
    try:
        users_to_check = [
            {"username": "admin", "password": "hdvn@dens0", "role": "admin"},
            {"username": "hv90122", "password": "hdvn@dens0", "role": "teacher"},
            {"username": "hv10921", "password": "hdvn@dens0", "role": "teacher"},
        ]
        seeded_any = False
        for u_data in users_to_check:
            user = User.query.filter_by(username=u_data["username"]).first()
            if not user:
                user = User(username=u_data["username"], password=u_data["password"], role=u_data["role"])
                db.session.add(user)
                seeded_any = True
        if seeded_any:
            db.session.commit()
            print("Seeded missing default users.")
        else:
            print("Default users already exist, skipping credentials override.")
    except Exception as e:
        db.session.rollback()
        print(f"Seed/update warning: {e}")


def _seed_quiz_options():
    """Seed the built-in quiz options and their steps."""
    from app.models.quiz_option import QuizOption
    from app.models.quiz_step import QuizStep
    
    # 1. OPTION 1
    try:
        option1 = QuizOption.query.filter_by(code="option1").first()
        if not option1:
            option1 = QuizOption(title="Kiểm tra thao tác đúc", code="option1", is_custom=False, quiz_format="option1")
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
                "1.Tay phải bóp vào vị trí của Slide\n trên conector.\n2.Các chân terminal nằm trên 1 mặt phẳng, khớp with chân pin  trên khuôn.",
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
        print(f"Option 1 seed warning: {e}")

    # 2. OPTION 3
    try:
        option3 = QuizOption.query.filter_by(code="option3").first()
        if not option3:
            option3 = QuizOption(title="Hành động xử lý bất thường", code="option3", is_custom=False, quiz_format="option3")
            db.session.add(option3)
            db.session.commit()

            device_texts = [
                "Công nhân phát hiện ra bất thường",
                "Nhận liên lạc về bất thường từ công nhân",
                "Xác nhận bất thường bằng hiện vật - hiện trường",
                "Dừng chuyền",
                "Yêu cầu bảo dưỡng đến sửa chữa",
                "Xác nhận ảnh hưởng đến công đoạn sau",
                "Liên lạc với cấp trên, nhận chỉ thị",
                "Liên lạc ảnh hưởng đến công đoạn sau",
                "Triển khai nội dung sự cố đến công nhân",
                "Xác nhận sau khi sửa chữa",
                "Triển khai kết quả sửa chữa đến công nhân",
                "Báo cáo kết quả xử lý đến cấp trên",
                "Chỉ thị tái sản xuất đến công nhân",
                "Liên lạc tái sản xuất đến công đoạn sau",
                "Triển khai nội dung sự cố đến bộ phận khác",
                "Thực hiện ngăn ngừa tái phát"
            ]

            quality_texts = [
                "Phát hiện bất thường",
                "Dừng - Gọi - Đợi",
                "Xác nhận bất thường bằng hiện vật hiện trường",
                "Liên lạc đến cấp trên",
                "Xác nhận tồn kho trong công đoạn",
                "Yêu cầu tạm dừng xuất hàng",
                "Chỉ thị kiểm tra phân loại sản phẩm OK, NG",
                "Chỉ thị kiểm tra phân loại đến công đoạn sau (Phán đoán dừng xuất hàng)",
                "Phân tích nguyên nhân",
                "Xác định nguyên nhân chính",
                "Yêu cầu hợp tác đến các bộ phận liên quan",
                "Lập đối sách",
                "Xử lý bất thường",
                "Báo cáo kết quả xử lý lên cấp trên",
                "Liên lạc kết quả xử lý đến công nhân",
                "Tái sản xuất",
                "Xác nhận chất lượng của 1 sản phẩm đầu",
                "Báo cáo đến công đoạn sau\nLàm bù phần bị chậm",
                "Thực hiện biện pháp ngăn ngừa tái phát",
                "Triển khai ngang"
            ]

            # Step 1..16: device
            for idx, text in enumerate(device_texts):
                step = QuizStep(
                    option_id=option3.id,
                    step_num=idx + 1,
                    image_url="",
                    left_text=text,
                    right_text="device",
                    note_text="",
                    reason_text=""
                )
                db.session.add(step)
            # Step 17..36: quality
            for idx, text in enumerate(quality_texts):
                step = QuizStep(
                    option_id=option3.id,
                    step_num=idx + 17,
                    image_url="",
                    left_text=text,
                    right_text="quality",
                    note_text="",
                    reason_text=""
                )
                db.session.add(step)
            db.session.commit()
            print("Seeded Option 3 successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Option 3 seed warning: {e}")

    # 3. OPTION 4
    try:
        option4 = QuizOption.query.filter_by(code="option4").first()
        if not option4:
            option4 = QuizOption(title="Kiểm tra chất lượng", code="option4", is_custom=False, quiz_format="option4")
            db.session.add(option4)
            db.session.commit()

            # Topic 1: 1..4
            t1_quants = ["2", "3", "2", "3"]
            for idx, q in enumerate(t1_quants):
                step = QuizStep(
                    option_id=option4.id,
                    step_num=idx + 1,
                    image_url="",
                    left_text=q,
                    right_text="",
                    note_text="",
                    reason_text=""
                )
                db.session.add(step)

            # Topic 2: 5..8
            t2_quants = ["3", "2", "3", "2"]
            for idx, q in enumerate(t2_quants):
                step = QuizStep(
                    option_id=option4.id,
                    step_num=idx + 5,
                    image_url="",
                    left_text=q,
                    right_text="",
                    note_text="",
                    reason_text=""
                )
                db.session.add(step)

            # Topic 3: 9..12 (Location, Status, Quantity)
            t3_data = [
                ("A", "D", "2"),
                ("B", "G", "2"),
                ("C", "E", "2"),
                ("D", "F", "1")
            ]
            for idx, (loc, stat, q) in enumerate(t3_data):
                step = QuizStep(
                    option_id=option4.id,
                    step_num=idx + 9,
                    image_url="",
                    left_text=loc,
                    right_text=stat,
                    note_text=q,
                    reason_text=""
                )
                db.session.add(step)

            # Topic 4: 13..16 (Location, Status, Quantity)
            t4_data = [
                ("2 tấm cánh", "Thiếu", "2"),
                ("Móng", "Bị đứt", "2"),
                ("Nắp", "Bị nứt", "1"),
                ("Móng", "Bị thiếu", "2")
            ]
            for idx, (loc, stat, q) in enumerate(t4_data):
                step = QuizStep(
                    option_id=option4.id,
                    step_num=idx + 13,
                    image_url="",
                    left_text=loc,
                    right_text=stat,
                    note_text=q,
                    reason_text=""
                )
                db.session.add(step)

            # Topic 5: 17..20 (Location, Status)
            t5_data = [
                ("C", "F"),
                ("G", "C"),
                ("A", "B"),
                ("D", "E")
            ]
            for idx, (loc, stat) in enumerate(t5_data):
                step = QuizStep(
                    option_id=option4.id,
                    step_num=idx + 17,
                    image_url="",
                    left_text=loc,
                    right_text=stat,
                    note_text="",
                    reason_text=""
                )
                db.session.add(step)

            # Topic 6: 21..24 (Location, Status)
            t6_data = [
                ("N", "sai số"),
                ("M", "không có,ngắn"),
                ("C", "cong"),
                ("B", "không có, thiếu")
            ]
            for idx, (loc, stat) in enumerate(t6_data):
                step = QuizStep(
                    option_id=option4.id,
                    step_num=idx + 21,
                    image_url="",
                    left_text=loc,
                    right_text=stat,
                    note_text="",
                    reason_text=""
                )
                db.session.add(step)

            # Topic 7: 25 (Image, Quantity)
            step_t7 = QuizStep(
                option_id=option4.id,
                step_num=25,
                image_url="/static/imgoptions4/hinh1.png",
                left_text="11",
                right_text="",
                note_text="",
                reason_text=""
            )
            db.session.add(step_t7)

            # Topic 8: 26 (Image, Quantity)
            step_t8 = QuizStep(
                option_id=option4.id,
                step_num=26,
                image_url="/static/imgoptions4/hinh2.png",
                left_text="11",
                right_text="",
                note_text="",
                reason_text=""
            )
            db.session.add(step_t8)

            db.session.commit()
            print("Seeded Option 4 successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Option 4 seed warning: {e}")

    # 4. OPTION 5 - Basic TIE category matching
    try:
        option5 = QuizOption.query.filter_by(code="option5").first()
        if not option5:
            option5 = QuizOption(
                title="Kiểm tra hạng mục cơ bản",
                code="option5",
                is_custom=False,
                quiz_format="option5"
            )
            db.session.add(option5)
            db.session.commit()

            matching_rows = [
                ("Biểu đồ quản lý công số", "Quản lý hiện trạng sản xuất đạt được hằng ngày."),
                ("Tiến độ sản xuất", "Xác nhận rõ sự tiến triển và chậm trễ của sản xuất"),
                ("Quản lý lượng tồn kho", "Phát hiện dị thường theo sự tăng giảm của lượng tồn kho"),
                ("Bản thao tác tiêu chuẩn", "Xác minh rõ về qui định thao tác"),
                ("Hiệu suất hoạt động", "Thông báo bất thường từ số sản lượng của mỗi giờ"),
                ("Bản quản lý sản lượng", "Cấu thành dây chuyền sản xuất\nCân bằng thời gian yêu cầu ở mỗi dây chuyền"),
                ("Bản kế hoạch cải tiến", "Đối sách về các vấn đề đã phát sinh trong thực tế"),
                ("Andon", "Thông báo chỉ thị thao tác, hiện trạng hoạt động của dây chuyền"),
            ]
            for idx, (category, role) in enumerate(matching_rows, start=1):
                db.session.add(QuizStep(
                    option_id=option5.id,
                    step_num=idx,
                    image_url="",
                    left_text=category,
                    right_text=role,
                    note_text="",
                    reason_text=""
                ))
            db.session.commit()
            print("Seeded Option 5 successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Option 5 seed warning: {e}")


