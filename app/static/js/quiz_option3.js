// ══════════════════════════════════════════════════════════
//  QUIZ OPTION 3: HÀNH ĐỘNG XỬ LÝ BẤT THƯỜNG
// ══════════════════════════════════════════════════════════

let o3Tab = 'device'; // 'device' or 'quality'
let o3DevicePool = []; // Shuffled texts for device steps (3..16)
let o3QualityPool = []; // Shuffled texts for quality steps (3..20)

// Answers stored as arrays of strings. Indexes match the 0-based step numbers.
let o3DeviceAnswers = Array(16).fill("");
let o3QualityAnswers = Array(20).fill("");

function initOption3() {
  // Pre-fill fixed steps
  o3DeviceAnswers[0] = activeQuizSteps[0] ? activeQuizSteps[0].left_text : "Công nhân phát hiện ra bất thường";
  o3DeviceAnswers[1] = activeQuizSteps[1] ? activeQuizSteps[1].left_text : "Nhận liên lạc về bất thường từ công nhân";

  o3QualityAnswers[0] = activeQuizSteps[16] ? activeQuizSteps[16].left_text : "Phát hiện bất thường";
  o3QualityAnswers[1] = activeQuizSteps[17] ? activeQuizSteps[17].left_text : "Dừng - Gọi - Đợi";

  // Build the pools once
  o3DevicePool = [];
  for (let i = 2; i < 16; i++) {
    if (activeQuizSteps[i]) {
      o3DevicePool.push(activeQuizSteps[i].left_text);
    }
  }
  o3DevicePool = shuffle(o3DevicePool);

  o3QualityPool = [];
  for (let i = 18; i < 36; i++) {
    if (activeQuizSteps[i]) {
      o3QualityPool.push(activeQuizSteps[i].left_text);
    }
  }
  o3QualityPool = shuffle(o3QualityPool);

  // Restore WIP if any
  const savedWip = localStorage.getItem('o3Answers_' + studentId);
  if (savedWip) {
    try {
      const parsed = JSON.parse(savedWip);
      if (parsed.device && parsed.device.length === 16) {
        o3DeviceAnswers = parsed.device;
      }
      if (parsed.quality && parsed.quality.length === 20) {
        o3QualityAnswers = parsed.quality;
      }
    } catch(e) {
      // ignore
    }
  }

  // Ensure fixed steps are not wiped out
  o3DeviceAnswers[0] = activeQuizSteps[0] ? activeQuizSteps[0].left_text : "Công nhân phát hiện ra bất thường";
  o3DeviceAnswers[1] = activeQuizSteps[1] ? activeQuizSteps[1].left_text : "Nhận liên lạc về bất thường từ công nhân";
  o3QualityAnswers[0] = activeQuizSteps[16] ? activeQuizSteps[16].left_text : "Phát hiện bất thường";
  o3QualityAnswers[1] = activeQuizSteps[17] ? activeQuizSteps[17].left_text : "Dừng - Gọi - Đợi";

  switchO3Tab('device');
  renderO3Steps();
  updateO3Progress();
}

function switchO3Tab(tab) {
  o3Tab = tab;
  const devTabBtn = document.getElementById('tabDeviceO3');
  const qualTabBtn = document.getElementById('tabQualityO3');
  const devPanel = document.getElementById('panelDeviceO3');
  const qualPanel = document.getElementById('panelQualityO3');

  if (tab === 'device') {
    devTabBtn.className = "px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition duration-200 bg-blue-600 text-white shadow-md shadow-blue-500/20";
    qualTabBtn.className = "px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition duration-200 bg-slate-800 text-slate-400 hover:text-white";
    devPanel.classList.remove('hidden');
    qualPanel.classList.add('hidden');
  } else {
    qualTabBtn.className = "px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition duration-200 bg-blue-600 text-white shadow-md shadow-blue-500/20";
    devTabBtn.className = "px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition duration-200 bg-slate-800 text-slate-400 hover:text-white";
    qualPanel.classList.remove('hidden');
    devPanel.classList.add('hidden');
  }
}

function renderO3Steps() {
  const devContainer = document.getElementById('deviceStepsList');
  const qualContainer = document.getElementById('qualityStepsList');

  // Render Device
  devContainer.innerHTML = '';
  for (let i = 0; i < 16; i++) {
    const isFixed = i < 2;
    const text = o3DeviceAnswers[i];
    const stepNum = i + 1;

    let cardHtml = "";
    if (isFixed) {
      cardHtml = `
        <div class="flex items-center gap-3 bg-emerald-500/10 border border-emerald-500/20 p-3 rounded-xl">
          <div class="w-7 h-7 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold text-xs">
            ${stepNum}
          </div>
          <div class="flex-1 text-sm font-semibold text-emerald-200">${text}</div>
          <span class="text-[10px] uppercase font-bold text-emerald-400 bg-emerald-500/20 px-2 py-0.5 rounded-md">Cố định</span>
        </div>
      `;
    } else {
      const isSelected = text !== "";
      const textVal = isSelected ? text : `Bấm để chọn bước ${stepNum}...`;
      const textStyle = isSelected ? 'text-white font-semibold' : 'text-slate-500 italic';
      const borderStyle = isSelected ? 'bg-slate-800 border-blue-500/40 hover:border-blue-500' : 'bg-slate-900/60 border-white/5 hover:border-white/20';
      
      cardHtml = `
        <div onclick="openO3Selector(${i})" class="flex items-center gap-3 border p-3 rounded-xl cursor-pointer transition active:scale-[0.99] ${borderStyle}">
          <div class="w-7 h-7 ${isSelected ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-400'} rounded-full flex items-center justify-center font-bold text-xs">
            ${stepNum}
          </div>
          <div class="flex-1 text-sm ${textStyle}">${textVal}</div>
          ${isSelected ? `
            <button onclick="event.stopPropagation(); clearO3Selection(${i})" class="text-xs text-red-400 hover:text-red-300 font-bold px-2 py-1 rounded bg-red-500/10 hover:bg-red-500/20 border border-red-500/20">
              Xóa
            </button>
          ` : `
            <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
            </svg>
          `}
        </div>
      `;
    }
    devContainer.innerHTML += cardHtml;
  }

  // Render Quality
  qualContainer.innerHTML = '';
  for (let j = 0; j < 20; j++) {
    const isFixed = j < 2;
    const text = o3QualityAnswers[j];
    const stepNum = j + 1;

    let cardHtml = "";
    if (isFixed) {
      cardHtml = `
        <div class="flex items-center gap-3 bg-emerald-500/10 border border-emerald-500/20 p-3 rounded-xl">
          <div class="w-7 h-7 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold text-xs">
            ${stepNum}
          </div>
          <div class="flex-1 text-sm font-semibold text-emerald-200">${text}</div>
          <span class="text-[10px] uppercase font-bold text-emerald-400 bg-emerald-500/20 px-2 py-0.5 rounded-md">Cố định</span>
        </div>
      `;
    } else {
      const isSelected = text !== "";
      const textVal = isSelected ? text : `Bấm để chọn bước ${stepNum}...`;
      const textStyle = isSelected ? 'text-white font-semibold' : 'text-slate-500 italic';
      const borderStyle = isSelected ? 'bg-slate-800 border-blue-500/40 hover:border-blue-500' : 'bg-slate-900/60 border-white/5 hover:border-white/20';

      cardHtml = `
        <div onclick="openO3Selector(${j})" class="flex items-center gap-3 border p-3 rounded-xl cursor-pointer transition active:scale-[0.99] ${borderStyle}">
          <div class="w-7 h-7 ${isSelected ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-400'} rounded-full flex items-center justify-center font-bold text-xs">
            ${stepNum}
          </div>
          <div class="flex-1 text-sm ${textStyle}">${textVal}</div>
          ${isSelected ? `
            <button onclick="event.stopPropagation(); clearO3Selection(${j})" class="text-xs text-red-400 hover:text-red-300 font-bold px-2 py-1 rounded bg-red-500/10 hover:bg-red-500/20 border border-red-500/20">
              Xóa
            </button>
          ` : `
            <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
            </svg>
          `}
        </div>
      `;
    }
    qualContainer.innerHTML += cardHtml;
  }
}

function openO3Selector(index) {
  const modal = document.getElementById('selectionModal');
  const title = document.getElementById('selectionTitle');
  const optionsDiv = document.getElementById('selectionOptions');
  const actionDiv = document.getElementById('selectionActions');

  title.textContent = `Chọn đối ứng bước ${index + 1} (${o3Tab === 'device' ? 'Thiết bị' : 'Chất lượng'})`;
  optionsDiv.innerHTML = '';

  const pool = o3Tab === 'device' ? o3DevicePool : o3QualityPool;
  const currentAnswers = o3Tab === 'device' ? o3DeviceAnswers : o3QualityAnswers;

  pool.forEach(text => {
    // Check if selected elsewhere
    const alreadyIdx = currentAnswers.indexOf(text);
    const isSelectedElsewhere = alreadyIdx !== -1 && alreadyIdx !== index;
    const isSelectedHere = currentAnswers[index] === text;

    let badge = "";
    if (isSelectedHere) {
      badge = `<span class="bg-blue-500 text-white text-[10px] font-bold px-2 py-0.5 rounded ml-2">Đang chọn</span>`;
    } else if (isSelectedElsewhere) {
      badge = `<span class="bg-slate-700 text-slate-400 text-[10px] font-bold px-2 py-0.5 rounded ml-2">Bị trùng ở bước ${alreadyIdx + 1}</span>`;
    }

    const card = document.createElement('div');
    card.className = `p-3 rounded-xl border text-sm transition cursor-pointer font-semibold ${
      isSelectedHere 
        ? 'bg-blue-600/10 border-blue-500 text-blue-200' 
        : 'bg-slate-900/60 border-white/5 text-slate-300 hover:bg-slate-800 hover:text-white'
    }`;
    card.innerHTML = `
      <div class="flex justify-between items-center">
        <span class="flex-1">${text}</span>
        ${badge}
      </div>
    `;
    card.onclick = () => {
      // Set value
      if (isSelectedElsewhere) {
        // Clear from previous index to prevent duplicates
        currentAnswers[alreadyIdx] = "";
      }
      currentAnswers[index] = text;
      
      saveO3Wip();
      renderO3Steps();
      updateO3Progress();
      closeSelectionModal();
    };
    optionsDiv.appendChild(card);
  });

  if (currentAnswers[index]) {
    actionDiv.classList.remove('hidden');
    document.getElementById('btnRemoveSelection').onclick = () => {
      clearO3Selection(index);
      closeSelectionModal();
    };
  } else {
    actionDiv.classList.add('hidden');
  }

  modal.classList.remove('hidden');
}

function clearO3Selection(index) {
  const currentAnswers = o3Tab === 'device' ? o3DeviceAnswers : o3QualityAnswers;
  currentAnswers[index] = "";
  saveO3Wip();
  renderO3Steps();
  updateO3Progress();
}

function saveO3Wip() {
  localStorage.setItem('o3Answers_' + studentId, JSON.stringify({
    device: o3DeviceAnswers,
    quality: o3QualityAnswers
  }));
}

function updateO3Progress() {
  // Count how many non-empty user inputs (device indices 2..15, quality indices 2..19)
  let devCount = 0;
  for (let i = 2; i < 16; i++) {
    if (o3DeviceAnswers[i]) devCount++;
  }

  let qualCount = 0;
  for (let j = 2; j < 20; j++) {
    if (o3QualityAnswers[j]) qualCount++;
  }

  const completed = devCount + qualCount;
  const progressText = document.getElementById('progressTextO3');
  progressText.textContent = `Đã hoàn thành: ${completed}/32 bước tự chọn`;

  const submitBtn = document.getElementById('submitBtnO3');
  // Always allow submission without completing all steps
  submitBtn.disabled = false;
}

async function submitOption3() {
  if (!confirm('Bạn có chắc chắn muốn nộp bài thi Hành động xử lý bất thường?')) return;
  const submitBtn = document.getElementById('submitBtnO3');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Đang chấm điểm...';

  try {
    const res = await fetch('/quiz/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        student_id: studentId,
        device_answers: o3DeviceAnswers,
        quality_answers: o3QualityAnswers
      })
    });
    const data = await res.json();
    if (!res.ok) {
      alert('Không thể nộp bài: ' + (data.detail || 'Lỗi hệ thống'));
      submitBtn.disabled = false;
      submitBtn.textContent = 'Nộp bài thi bất thường';
      return;
    }

    localStorage.setItem('submitted_' + studentId, 'true');
    localStorage.setItem('results_' + studentId, JSON.stringify(data));

    showO3Results(data);
  } catch (err) {
    alert('Lỗi kết nối: ' + err.message);
    submitBtn.disabled = false;
    submitBtn.textContent = 'Nộp bài thi bất thường';
  }
}

function showO3Results(data) {
  document.getElementById('screenOption3').classList.add('hidden');
  document.getElementById('screenResult').classList.remove('hidden');

  const pct = Math.round((data.score / 36) * 100);
  const emoji = pct === 100 ? '🏆' : pct >= 70 ? '🎉' : pct >= 40 ? '👍' : '💪';
  const title = pct === 100 ? 'Hoàn hảo!' : pct >= 70 ? 'Xuất sắc!' : pct >= 40 ? 'Khá tốt!' : 'Cố gắng hơn!';

  document.getElementById('resultEmoji').textContent = emoji;
  document.getElementById('resultTitle').textContent = title;
  document.getElementById('resultSub').textContent = `${studentName} – ${data.score}/36 đúng (${pct}%)`;
  document.getElementById('scoreDisplay').textContent = `${data.score}/36`;

  const detail = document.getElementById('answerDetail');
  detail.innerHTML = `
    <div class="flex justify-between items-center py-1 border-b border-gray-100">
      <span class="font-semibold text-gray-700">Trang 1: Sự cố thiết bị</span>
      <span class="font-bold text-blue-600">${data.device_score}/16 điểm</span>
    </div>
    <div class="flex justify-between items-center py-1">
      <span class="font-semibold text-gray-700">Trang 2: Sự cố chất lượng</span>
      <span class="font-bold text-blue-600">${data.quality_score}/20 điểm</span>
    </div>
  `;
}
