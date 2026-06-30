// ═══════════════════════════════════════════════════════
//  GLOBAL DATA & DATA STRUCTURES
// ═══════════════════════════════════════════════════════
const SUB_QUIZ_DATA = {
  1: {
    title: "Bài 1: Cơ bản TIE",
    type: "matching",
    left: ["Just in time", "Tự động hóa", "Thao tác tiêu chuẩn", "Kanban", "Lãng phí (Muda)"],
    right: [
      { id: "A", text: "Là một trong 2 phương thức sản xuất của Toyota nhằm nâng cao hiệu quả kinh doanh và là quan niệm của cơ chế sản xuất như chỉ sản xuất , vận chuyển vật cần thiết tại thời gian cần thiết" },
      { id: "B", text: "Là 1 trong hai phương thức sản xuất Toyota nhằm để phát hiện ra bất thường thiết bị , và bất cứ bất thường nào phát sinh như chất lượng , thiết bị , khi đó máy sẽ tự động phát hiện và dừng lại hoặc người thao tác chỉ cần ấn công tắc dừng và dây chuyên sẽ được dừng lại." },
      { id: "C", text: "Là phương pháp thực hiện sản xuất một cách hiệu quả ở trình tự không có lãng phí và tập trung vào động tác của người thao tác. Bao gồm 3 yếu tố như tiêu chuẩn cầm tay , trình tự thao tác , takt time." },
      { id: "D", text: "Giữ vai trò ở công cụ quản lý kiểm tra bằng mắt, công cụ của thao tác, cải tiến công đoạn, báo cáo chỉ thị về vận chuyển, sản xuất. Là công cụ quản lý để thực hiện sản xuất theo just in time" },
      { id: "E", text: "Tất cả những thứ thêm vào mà không làm gia tăng giá trị vật" }
    ],
    correct: { 0: "A", 1: "B", 2: "C", 3: "D", 4: "E" }
  },
  2: {
    title: "Bài 2: 7 loại lãng phí",
    type: "matching",
    left: ["Lãng phí ở động tác", "Lãng phí khi vận chuyển", "Lãng phí do sản xuất quá nhiều", "Lãng phí do chờ tay", "Lãng phí gia công", "Lãng phí tồn kho", "Lãng phí do làm, sửa lại"],
    right: [
      { id: "A", text: "lãng phí khi đi lấy hoặc đi tìm công cụ trong khi làm việc, vị trí xếp đặt linh kiện, công cụ không hợp lý sẽ làm phát sinh ra các động tác dư thừa" },
      { id: "B", text: "Là lãng phí phát sinh do khoảng cách vận chuyển không hợp lý hay do trung chuyển , đặt để tạm thời." },
      { id: "C", text: "Là tình trạng tồn kho phát sinh do sản xuất vượt quá lượng đã được chỉ định ở Kanban, sản xuất nhanh hơn so với thời điểm phù hợp , cần thiết. Và là lãng phí quan trọng che lấp đi các vấn đề lãng phí khác." },
      { id: "D", text: "Là lãng phí khi người thao tác đang trong trạng thái chờ không làm việc do thiết bị đang gia công hoặc sự cân bằng trong công đoạn không đồng đều , lượng công việc ít…" },
      { id: "E", text: "Là lãng phí thực hiện gia công không cần thiết ,không đóng góp gì cho sự tiến triển của công đoạn, độ chính xác của vật …" },
      { id: "F", text: "Là lãng phí tồn kho (thành phẩm giữa các công đoạn, nguyên vật liệu) phát sinh do cơ cấu vận chuyển, sản xuất." },
      { id: "G", text: "lãng phí do thao tác sửa chữa lại các vật , phế phẩm đã bị hoàn trả lại ." }
    ],
    correct: { 0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G" }
  },
  3: {
    title: "Bài 3: Phân tích thời gian ・Tốc độ thao tác",
    type: "matching",
    left: ["Phân tích thời gian thao tác yếu tố", "Quan sát đo liên tục", "Chờ tay", "Tốc độ tiêu chuẩn", "Tốc độ bình thường"],
    right: [
      { id: "A", text: "Được áp dụng ở việc quan sát thao tác trong thời gian ngắn, theo qui tắc , tính lặp lại cao , và là 1 phương pháp của việc phân tích thời gian" },
      { id: "B", text: "Được áp dụng ở việc quan sát lâu ở thời gian có tính lặp lại nhiều lần hoặc ít tính lặp lại và là 1 phương pháp của phân tích thời gian" },
      { id: "C", text: "Là trạng thái người thao tác đứng chờ việc cho dù thực hiện công việc theo đúng trình tự của thao tác tiêu chuẩn" },
      { id: "D", text: "Là tốc độ thao tác nhanh, có ý thức cố gắng làm việc chăm chỉ." },
      { id: "E", text: "Là tốc độ mà người thao tác vừa làm vừa suy nghĩ về vấn đề khác" }
    ],
    correct: { 0: "A", 1: "B", 2: "C", 3: "D", 4: "E" }
  },
  4: {
    title: "Bài 4: Thao tác tiêu chuẩn",
    type: "matching",
    left: ["Trình tự thao tác", "Machine time", "Tiêu chuẩn chờ tay", "Phiếu kết hợp thao tác tiêu chuẩn", "Takt time"],
    right: [
      { id: "A", text: "Là 1 trong 3 yếu tố của thao tác tiêu chuẩn , và là trình tự thao tác mà người thao tác có thể sản suất ra sản phẩm tốt một cách hiệu quả nhất." },
      { id: "B", text: "Là thời gian cần thiết của máy để gia công ra 1 sản phẩm. Ở các máy thông thường thì, sau khi ấn nút khởi động thì máy sẽ thực hiện gia công sản phẩm , và sẽ tự động khôi phục lại ở vị trí ban đầu" },
      { id: "C", text: "Là 1 trong 3 yếu tố của thao tác tiêu chuẩn, thực hiện cầm vật với thao tác , động tác, thứ tự lặp đi lặp lại giống nhau trong giới hạn tối thiểu nhất." },
      { id: "D", text: "Là vật điều tra rõ thời gian di chuyển và thời gian thao tác tay của mỗi công đoạn mà 1 người thao tác có thể đảm nhận trong phạm vi như thế nào trong Takt time." },
      { id: "E", text: "Là giá trị thời gian phải mất bao lâu để sản xuất ra 1 sản phẩm hoặc 1 linh kiện" }
    ],
    correct: { 0: "A", 1: "B", 2: "C", 3: "D", 4: "E" }
  },
  5: {
    title: "Bài 5: Mục đích phân tích động tác",
    type: "fill",
    text: "Động tác ・thao tác được nhìn quen mỗi ngày thì có thể nhớ nhưng những lãng phí của động tác nhỏ thì hầu như không nhìn thấy được. Và vì là những lãng phí nhỏ nên hầu như ai cũng nghĩ rằng sẽ không gây ảnh hưởng đến năng suất sản xuất. Tuy nhiên nếu tích tụ {0} lại và thực hiện trong 1 ngày thì sẽ là nguyên nhân dẫn đến {1}.",
    options: ["những lãng phí nhỏ", "Tổn thất lớn về thời gian", "Lợi ích lớn"],
    correct: { 0: "những lãng phí nhỏ", 1: "Tổn thất lớn về thời gian" }
  },
  6: {
    title: "Bài 6: Cấu thành thao tác",
    type: "single_choice_image",
    image: "/static/q7.png",
    options: ["(A)", "(B)", "(C)", "(D)"],
    correct: { 0: "(D)" }
  },
  7: {
    title: "Bài 7: 4 nguyên tắc cải thiện",
    type: "custom_inputs_image",
    image: "/static/q71.png",
    desc: "Nhập chữ cái đúng (A, B, C, D, E) cho 4 nguyên tắc từ trên xuống dưới:",
    placeholder: "Nhập chữ cái...",
    inputs: ["Nguyên tắc 1", "Nguyên tắc 2", "Nguyên tắc 3", "Nguyên tắc 4"],
    correct: { "Nguyên tắc 1": "C", "Nguyên tắc 2": "A", "Nguyên tắc 3": "D", "Nguyên tắc 4": "E" }
  },
  8: {
    title: "Bài 8: Cải thiện động tác cơ bản",
    type: "tf",
    image: "/static/q8.png",
    desc: "Hãy chọn O vào vấn đề đúng và đánh dấu X vào vấn đề sai về phương pháp quan sát động tác",
    questions: [
      { id: "1", text: "Độ khó của động tác" },
      { id: "2", text: "Độ dễ của động tác" },
      { id: "3", text: "Độ lớn của động tác" },
      { id: "4", text: "Trình tự của động tác" },
      { id: "5", text: "Phương pháp của động tác" }
    ],
    correct: { "1": "O", "2": "X", "3": "O", "4": "O", "5": "X" }
  },
  9: {
    title: "Bài 9: Giới hạn sản lượng",
    type: "custom_inputs_image",
    image: "/static/q10.png",
    desc: "Nhập số thích hợp vào các ô từ 1 đến 10:",
    inputs: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    correct: {
      "1": "20",
      "2": "180",
      "3": "180",
      "4": "90",
      "5": "162",
      "6": "20",
      "7": "150",
      "8": "150",
      "9": "90",
      "10": "135"
    }
  }

};

const O1_TEXTS = {
  left: [
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
  ],
  right: [
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
  ],
  note: [
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
    "1. Hướng nhãn màu \ncam về phía người thao tác\n2.Chân jig khớp với các lỗ \ntrên khuôn \n3.Nhấc jig, chân jig cao hơn đầu conector",
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
  ],
  reason: [
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
};
