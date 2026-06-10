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
    left: ["Trình tự thao tác", "Machine time", "Tiêu chuẩn cầm tay", "Phiếu kết hợp thao tác tiêu chuẩn", "Takt time"],
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
    title: "Bài 5: 8 hạng mục cơ bản",
    type: "matching",
    left: [
      "Bản quản lý sản lượng", "Bản kế hoạch cải tiến", "Bản thao tác tiêu chuẩn", "Andon", "Tiến độ sản xuất",
      "Quản lý lượng tồn kho", "Hiệu xuất hoạt động", "Biểu đồ quản lý công số", "Cấu thành dây chuyền sản xuất"
    ],
    right: [
      { id: "A", text: "Thông báo bất thường từ sản lượng của mỗi giờ" },
      { id: "B", text: "Đối sách về các vấn đề đã phát sinh trong thực tế" },
      { id: "C", text: "Xác minh rõ về qui định thao tác" },
      { id: "D", text: "Thông báo chỉ thị thao tác, Hiện trạng hoạt động của dây chuyền" },
      { id: "E", text: "Xác nhận rõ sự tiến triễn và chậm trễ của sản xuất" },
      { id: "F", text: "Phát hiện bất thường theo sự tăng giảm của lượng tồn kho" },
      { id: "G", text: "Xác minh rõ về nguyên nhân chính không hoạt động của thiết bị" },
      { id: "H", text: "Quản lý hiện trạng sản xuất đạt được hằng ngày." },
      { id: "I", text: "Cân bằng thời gian yêu cầu ở mỗi dây chuyền" }
    ],
    correct: { 0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I" }
  },
  6: {
    title: "Bài 6: Mục đích phân tích động tác",
    type: "fill",
    text: "Động tác ・thao tác được nhìn quen mỗi ngày thì có thể nhớ nhưng những lãng phí của động tác nhỏ thì hầu như không nhìn thấy được. Và vì là những lãng phí nhỏ nên hầu như ai cũng nghĩ rằng sẽ không gây ảnh hưởng đến năng suất sản xuất. Tuy nhiên nếu tích tụ {0} lại và thực hiện trong 1 ngày thì sẽ là nguyên nhân dẫn đến {1}.",
    options: ["những lãng phí nhỏ", "Tổn thất lớn về thời gian", "Lợi ích lớn"],
    correct: { 0: "những lãng phí nhỏ", 1: "Tổn thất lớn về thời gian" }
  },
  7: {
    title: "Bài 7: Cấu thành thao tác",
    type: "matching",
    left: ["Thao tác (công đoạn)", "Thao tác đơn vị", "Thao tác yếu tố", "Động tác cơ bản"],
    right: [
      { id: "A", text: "B/K lắp ráp" },
      { id: "B", text: "Lấy ốc rồi dùng tua vít để lắp ốc vào" },
      { id: "C", text: "Thao tác lắp vào" },
      { id: "D", text: "Đưa tay đến lấy ốc" }
    ],
    correct: { 0: "A", 1: "B", 2: "C", 3: "D" }
  },
  8: {
    title: "Bài 8: 4 nguyên tắc cải thiện",
    type: "matching",
    left: ["Loại bỏ (Lượt bớt)", "Kết hợp", "Thay thế (Thay đổi)", "Đơn giản"],
    right: [
      { id: "A", text: "If loại bỏ vật lãng phí hoặc dừng thao tác không cần thiết (Ví dụ: Loại bỏ kiểm tra bề ngoài không cần thiết)" }, // Wait, check if there was 'Nếu' or 'If' in original. Original had: "Nếu loại bỏ vật lãng phí..." let's check line 561: "Nếu loại bỏ vật lãng phí..."
      { id: "B", text: "Nếu thử thu thập, kết hợp lại hoặc thực hiện đồng thời (Ví dụ: Đồng thời hóa việc khoan lỗ với việc ép dập)" },
      { id: "C", text: "Nếu thay thế trình tự, thay đổi cách làm hoặc thay thế vật khác (Ví dụ: Mang đến phía trước công đoạn kiểm tra)" },
      { id: "D", text: "Nếu làm ngắn gọn, đơn giản hoặc giảm số lượng (Ví dụ: Phân công việc đảm nhiệm, làm một cách đơn giản)" }
    ],
    correct: { 0: "A", 1: "B", 2: "C", 3: "D" }
  },
  9: {
    title: "Bài 9: Cải thiện động tác cơ bản",
    type: "tf",
    questions: [
      { id: "1", text: "Trình tự của động tác là phương pháp quan sát động tác Đúng?" },
      { id: "2", text: "Độ lớn của động tác là phương pháp quan sát động tác Đúng?" },
      { id: "3", text: "Độ dễ của động tác là phương pháp quan sát động tác Đúng?" },
      { id: "4", text: "Độ khó của động tác là phương pháp quan sát động tác Đúng?" },
      { id: "5", text: "Phương pháp quan sát động tác là phương pháp quan sát động tác Đúng?" }
    ],
    correct: { "1": "O", "2": "X", "3": "O", "4": "O", "5": "O" }
  },
  10: {
    title: "Bài 10: Giới hạn sản lượng",
    type: "tf",
    questions: [
      { id: "1", text: "Thời gian 50 phút: Số cái mục tiêu (100%):" },
      { id: "2", text: "Thời gian 50 phút: Số cái giới hạn quản lý (90%):" },
      { id: "3", text: "Thời gian 60 phút: Số cái mục tiêu (100%):" },
      { id: "4", text: "Thời gian 60 phút: Số cái giới hạn quản lý (90%):" }
    ],
    options: ["150", "135", "180", "162", "200", "90"],
    correct: { "1": "150", "2": "135", "3": "180", "4": "162" }
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
    "Lấy terminal dài từ khay"
  ],
  right: [
    "—",
    "Đặt Terminal SA lên bề mặt khuôn ngoài",
    "Lấy sản phẩm từ khuôn đặt vào băng tải",
    "Lấy terminal S/A set vào khuôn ngoài",
    "Lấy terminal ngắn từ khay",
    "Set terminal ngắn vào khuôn trong",
    "Lấy terminal dài từ khay"
  ],
  note: [
    "Đảm bảo an toàn khi thao tác:\n1. Mũ đội chùm kín tóc\n2.Đeo kính không được trễ xuống mũi\n3.Gang tay, xỏ tay không rách thủng, đeo xỏ tay phải qua khủy tay, không để lộ cánh tay\n4. Giày bảo hộ thắt nút buộc dây chặt chẽ",
    "1.Khi đèn xanh sáng mới được vào thao tác\nKhông làm va linh kiện vào các vị trí trên khuôn",
    "1.Nhấc sản phẩm trước khi chân pin hạ xuống hết , nhấc vuông góc.\n2. Đặt 2 sản phẩm cùng chiều, không xếp chồng lên nhau và phần conector hướng về phía người thao tác đúc.",
    "1. Lỗ trên terminal khớp với chân pin trên khuôn.\n2. Ngón tay cái ấn các lỗ pin từ phía IC ra tới đầu các chân terminal.",
    "Terminal không bị cong.",
    "Xác nhận lỗ trên terminal khớp với chân pin trên khuôn.",
    "Terminal không bị cong."
  ],
  reason: [
    "1. Tránh dị vật tóc rơi vào sản phẩm.\n2.Dị vật bắn vào mắt\n3. Chạm vào vật có nhiệt độ cao gây bỏng tay.\n4.Vấp ngã khi thao tác",
    "NG linh kiện",
    "1. Máy báo lỗi , mất an toàn\n2&3 .Sản phẩm bị xước",
    "Tạo phế phẩm : Lộ terminal",
    "Tạo phế phẩm:\nCong terminal không set vào khuôn được",
    "Tạo phế phẩm:\nNhựa phủ moter terminal, Terminal bị lộ",
    "Tạo phế phẩm:\nCong terminal không set vào khuôn được"
  ]
};
