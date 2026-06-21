// ══════════════════════════════════════════════════════════
//  QUIZ OPTION 4: KIỂM TRA CHẤT LƯỢNG
// ══════════════════════════════════════════════════════════

let o4Tab = 'odd'; // 'odd' or 'even'
let o4SelectedT7Image = "";
let o4SelectedT8Image = "";
let o4ImagesList = [];

function initOption4() {
  // Generate rows for Topics 3, 4, 5, 6
  generateO4Rows();
  
  // Load defect images choices
  loadImgOptions4();

  // Attach change listeners to save WIP
  attachO4WipListeners();

  // Switch to default tab
  switchO4Tab('odd');
  
  // Restore saved WIP if any
  restoreO4Wip();
}

function switchO4Tab(tab) {
  o4Tab = tab;
  const oddTabBtn = document.getElementById('tabOddO4');
  const evenTabBtn = document.getElementById('tabEvenO4');
  const oddPanel = document.getElementById('panelOddO4');
  const evenPanel = document.getElementById('panelEvenO4');

  if (tab === 'odd') {
    oddTabBtn.className = "px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition duration-200 bg-blue-600 text-white shadow-md shadow-blue-500/20";
    evenTabBtn.className = "px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition duration-200 bg-slate-800 text-slate-400 hover:text-white";
    oddPanel.classList.remove('hidden');
    evenPanel.classList.add('hidden');
  } else {
    evenTabBtn.className = "px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition duration-200 bg-blue-600 text-white shadow-md shadow-blue-500/20";
    oddTabBtn.className = "px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition duration-200 bg-slate-800 text-slate-400 hover:text-white";
    evenPanel.classList.remove('hidden');
    oddPanel.classList.add('hidden');
  }
}

function generateO4Rows() {
  // Topic 3
  let t3Html = "";
  for (let i = 1; i <= 4; i++) {
    t3Html += `
      <div class="flex items-center gap-3 bg-slate-900/30 p-3 rounded-xl border border-white/5">
        <span class="w-6 h-6 bg-slate-800 text-slate-400 font-bold rounded-full flex items-center justify-center text-xs">${i}</span>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 flex-1">
          <div>
            <label class="block sm:hidden text-[9px] text-slate-400 font-bold uppercase mb-1">Vị trí lỗi</label>
            <input type="text" id="o4_t3_loc_${i}" class="w-full bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition" placeholder="Vị trí" />
          </div>
          <div>
            <label class="block sm:hidden text-[9px] text-slate-400 font-bold uppercase mb-1">Tình trạng lỗi</label>
            <input type="text" id="o4_t3_stat_${i}" class="w-full bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition" placeholder="Tình trạng" />
          </div>
          <div>
            <label class="block sm:hidden text-[9px] text-slate-400 font-bold uppercase mb-1">Số lượng</label>
            <input type="number" id="o4_t3_q_${i}" min="0" class="w-full bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-xs text-white font-bold text-center focus:outline-none focus:border-blue-500 transition" placeholder="Số lượng" />
          </div>
        </div>
      </div>
    `;
  }
  document.getElementById('t3RowsContainer').innerHTML = t3Html;

  // Topic 4
  let t4Html = "";
  for (let i = 1; i <= 4; i++) {
    t4Html += `
      <div class="flex items-center gap-3 bg-slate-900/30 p-3 rounded-xl border border-white/5">
        <span class="w-6 h-6 bg-slate-800 text-slate-400 font-bold rounded-full flex items-center justify-center text-xs">${i}</span>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 flex-1">
          <div>
            <label class="block sm:hidden text-[9px] text-slate-400 font-bold uppercase mb-1">Vị trí lỗi</label>
            <input type="text" id="o4_t4_loc_${i}" class="w-full bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition" placeholder="Vị trí" />
          </div>
          <div>
            <label class="block sm:hidden text-[9px] text-slate-400 font-bold uppercase mb-1">Tình trạng lỗi</label>
            <input type="text" id="o4_t4_stat_${i}" class="w-full bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition" placeholder="Tình trạng" />
          </div>
          <div>
            <label class="block sm:hidden text-[9px] text-slate-400 font-bold uppercase mb-1">Số lượng</label>
            <input type="number" id="o4_t4_q_${i}" min="0" class="w-full bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-xs text-white font-bold text-center focus:outline-none focus:border-blue-500 transition" placeholder="Số lượng" />
          </div>
        </div>
      </div>
    `;
  }
  document.getElementById('t4RowsContainer').innerHTML = t4Html;

  // Topic 5
  let t5Html = "";
  for (let i = 1; i <= 4; i++) {
    t5Html += `
      <div class="flex items-center gap-3 bg-slate-900/30 p-3 rounded-xl border border-white/5">
        <span class="w-6 h-6 bg-slate-800 text-slate-400 font-bold rounded-full flex items-center justify-center text-xs">${i}</span>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 flex-1">
          <div>
            <label class="block sm:hidden text-[9px] text-slate-400 font-bold uppercase mb-1">Vị trí lỗi</label>
            <input type="text" id="o4_t5_loc_${i}" class="w-full bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition" placeholder="Vị trí" />
          </div>
          <div>
            <label class="block sm:hidden text-[9px] text-slate-400 font-bold uppercase mb-1">Tình trạng lỗi</label>
            <input type="text" id="o4_t5_stat_${i}" class="w-full bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition" placeholder="Tình trạng" />
          </div>
        </div>
      </div>
    `;
  }
  document.getElementById('t5RowsContainer').innerHTML = t5Html;

  // Topic 6
  let t6Html = "";
  for (let i = 1; i <= 4; i++) {
    t6Html += `
      <div class="flex items-center gap-3 bg-slate-900/30 p-3 rounded-xl border border-white/5">
        <span class="w-6 h-6 bg-slate-800 text-slate-400 font-bold rounded-full flex items-center justify-center text-xs">${i}</span>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 flex-1">
          <div>
            <label class="block sm:hidden text-[9px] text-slate-400 font-bold uppercase mb-1">Vị trí lỗi</label>
            <input type="text" id="o4_t6_loc_${i}" class="w-full bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition" placeholder="Vị trí" />
          </div>
          <div>
            <label class="block sm:hidden text-[9px] text-slate-400 font-bold uppercase mb-1">Tình trạng lỗi</label>
            <input type="text" id="o4_t6_stat_${i}" class="w-full bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition" placeholder="Tình trạng" />
          </div>
        </div>
      </div>
    `;
  }
  document.getElementById('t6RowsContainer').innerHTML = t6Html;
}

async function loadImgOptions4() {
  try {
    const res = await fetch('/quiz/imgoptions4');
    if (!res.ok) return;
    const images = await res.json();
    o4ImagesList = images;
    
    // Topic 7 choices
    const t7Div = document.getElementById('t7ImagesContainer');
    if (t7Div) {
      t7Div.innerHTML = images.map(img => {
        const filename = img.split('/').pop();
        return `
          <div onclick="selectO4Image('t7', '${img}')" id="t7_img_${filename}" 
               class="border-2 border-white/10 hover:border-white/30 rounded-2xl overflow-hidden p-2 cursor-pointer transition active:scale-[0.98] bg-slate-900/40 hover:bg-slate-900/60 flex flex-col items-center gap-1">
            <img src="${img}" class="h-20 object-contain rounded-lg" />
            <span class="text-[10px] text-slate-400 font-bold">${filename}</span>
          </div>
        `;
      }).join('');
    }

    // Topic 8 choices
    const t8Div = document.getElementById('t8ImagesContainer');
    if (t8Div) {
      t8Div.innerHTML = images.map(img => {
        const filename = img.split('/').pop();
        return `
          <div onclick="selectO4Image('t8', '${img}')" id="t8_img_${filename}" 
               class="border-2 border-white/10 hover:border-white/30 rounded-2xl overflow-hidden p-2 cursor-pointer transition active:scale-[0.98] bg-slate-900/40 hover:bg-slate-900/60 flex flex-col items-center gap-1">
            <img src="${img}" class="h-20 object-contain rounded-lg" />
            <span class="text-[10px] text-slate-400 font-bold">${filename}</span>
          </div>
        `;
      }).join('');
    }

    highlightO4Images();
  } catch(e) {
    console.error("Error fetching imgoptions4", e);
  }
}

function selectO4Image(topic, url) {
  if (topic === 't7') {
    o4SelectedT7Image = url;
  } else {
    o4SelectedT8Image = url;
  }
  highlightO4Images();
  saveO4Wip();
}

function highlightO4Images() {
  o4ImagesList.forEach(img => {
    const filename = img.split('/').pop();
    // T7
    const t7El = document.getElementById(`t7_img_${filename}`);
    if (t7El) {
      if (o4SelectedT7Image === img || o4SelectedT7Image.endsWith(filename)) {
        t7El.className = "border-2 border-blue-500 bg-blue-500/10 rounded-2xl overflow-hidden p-2 cursor-pointer transition flex flex-col items-center gap-1";
      } else {
        t7El.className = "border-2 border-white/10 hover:border-white/30 rounded-2xl overflow-hidden p-2 cursor-pointer transition active:scale-[0.98] bg-slate-900/40 hover:bg-slate-900/60 flex flex-col items-center gap-1";
      }
    }
    // T8
    const t8El = document.getElementById(`t8_img_${filename}`);
    if (t8El) {
      if (o4SelectedT8Image === img || o4SelectedT8Image.endsWith(filename)) {
        t8El.className = "border-2 border-blue-500 bg-blue-500/10 rounded-2xl overflow-hidden p-2 cursor-pointer transition flex flex-col items-center gap-1";
      } else {
        t8El.className = "border-2 border-white/10 hover:border-white/30 rounded-2xl overflow-hidden p-2 cursor-pointer transition active:scale-[0.98] bg-slate-900/40 hover:bg-slate-900/60 flex flex-col items-center gap-1";
      }
    }
  });
}

function collectO4Answers() {
  // Topic 1
  const t1 = [];
  for (let i = 1; i <= 4; i++) {
    const val = document.getElementById(`o4_t1_q${i}`)?.value || "";
    t1.push(val);
  }

  // Topic 2
  const t2 = [];
  for (let i = 1; i <= 4; i++) {
    const val = document.getElementById(`o4_t2_q${i}`)?.value || "";
    t2.push(val);
  }

  // Topic 3
  const t3 = [];
  for (let i = 1; i <= 4; i++) {
    t3.push({
      loc: document.getElementById(`o4_t3_loc_${i}`)?.value || "",
      stat: document.getElementById(`o4_t3_stat_${i}`)?.value || "",
      quant: document.getElementById(`o4_t3_q_${i}`)?.value || ""
    });
  }

  // Topic 4
  const t4 = [];
  for (let i = 1; i <= 4; i++) {
    t4.push({
      loc: document.getElementById(`o4_t4_loc_${i}`)?.value || "",
      stat: document.getElementById(`o4_t4_stat_${i}`)?.value || "",
      quant: document.getElementById(`o4_t4_q_${i}`)?.value || ""
    });
  }

  // Topic 5
  const t5 = [];
  for (let i = 1; i <= 4; i++) {
    t5.push({
      loc: document.getElementById(`o4_t5_loc_${i}`)?.value || "",
      stat: document.getElementById(`o4_t5_stat_${i}`)?.value || ""
    });
  }

  // Topic 6
  const t6 = [];
  for (let i = 1; i <= 4; i++) {
    t6.push({
      loc: document.getElementById(`o4_t6_loc_${i}`)?.value || "",
      stat: document.getElementById(`o4_t6_stat_${i}`)?.value || ""
    });
  }

  return {
    odd_answers: {
      t1: t1,
      t3: t3,
      t5: t5,
      t7: { image_url: o4SelectedT7Image, quant: document.getElementById('o4_t7_quant')?.value || "" }
    },
    even_answers: {
      t2: t2,
      t4: t4,
      t6: t6,
      t8: { image_url: o4SelectedT8Image, quant: document.getElementById('o4_t8_quant')?.value || "" }
    }
  };
}

function saveO4Wip() {
  const answers = collectO4Answers();
  localStorage.setItem('o4Answers_' + studentId, JSON.stringify(answers));
}

function attachO4WipListeners() {
  const container = document.getElementById('screenOption4');
  if (container) {
    container.querySelectorAll('input').forEach(input => {
      input.removeEventListener('input', saveO4Wip);
      input.addEventListener('input', saveO4Wip);
    });
  }
}

function restoreO4Wip() {
  const saved = localStorage.getItem('o4Answers_' + studentId);
  if (!saved) return;
  try {
    const data = JSON.parse(saved);

    // Topic 1
    const t1 = data.odd_answers?.t1 || [];
    for (let i = 1; i <= 4; i++) {
      const el = document.getElementById(`o4_t1_q${i}`);
      if (el) el.value = t1[i-1] !== undefined ? t1[i-1] : "";
    }

    // Topic 2
    const t2 = data.even_answers?.t2 || [];
    for (let i = 1; i <= 4; i++) {
      const el = document.getElementById(`o4_t2_q${i}`);
      if (el) el.value = t2[i-1] !== undefined ? t2[i-1] : "";
    }

    // Topic 3
    const t3 = data.odd_answers?.t3 || [];
    for (let i = 1; i <= 4; i++) {
      const row = t3[i-1] || {};
      const loc = document.getElementById(`o4_t3_loc_${i}`);
      const stat = document.getElementById(`o4_t3_stat_${i}`);
      const q = document.getElementById(`o4_t3_q_${i}`);
      if (loc) loc.value = row.loc || "";
      if (stat) stat.value = row.stat || "";
      if (q) q.value = row.quant !== undefined ? row.quant : "";
    }

    // Topic 4
    const t4 = data.even_answers?.t4 || [];
    for (let i = 1; i <= 4; i++) {
      const row = t4[i-1] || {};
      const loc = document.getElementById(`o4_t4_loc_${i}`);
      const stat = document.getElementById(`o4_t4_stat_${i}`);
      const q = document.getElementById(`o4_t4_q_${i}`);
      if (loc) loc.value = row.loc || "";
      if (stat) stat.value = row.stat || "";
      if (q) q.value = row.quant !== undefined ? row.quant : "";
    }

    // Topic 5
    const t5 = data.odd_answers?.t5 || [];
    for (let i = 1; i <= 4; i++) {
      const row = t5[i-1] || {};
      const loc = document.getElementById(`o4_t5_loc_${i}`);
      const stat = document.getElementById(`o4_t5_stat_${i}`);
      if (loc) loc.value = row.loc || "";
      if (stat) stat.value = row.stat || "";
    }

    // Topic 6
    const t6 = data.even_answers?.t6 || [];
    for (let i = 1; i <= 4; i++) {
      const row = t6[i-1] || {};
      const loc = document.getElementById(`o4_t6_loc_${i}`);
      const stat = document.getElementById(`o4_t6_stat_${i}`);
      if (loc) loc.value = row.loc || "";
      if (stat) stat.value = row.stat || "";
    }

    // Topic 7
    const t7 = data.odd_answers?.t7 || {};
    o4SelectedT7Image = t7.image_url || "";
    const t7q = document.getElementById('o4_t7_quant');
    if (t7q) t7q.value = t7.quant !== undefined ? t7.quant : "";

    // Topic 8
    const t8 = data.even_answers?.t8 || {};
    o4SelectedT8Image = t8.image_url || "";
    const t8q = document.getElementById('o4_t8_quant');
    if (t8q) t8q.value = t8.quant !== undefined ? t8.quant : "";

    highlightO4Images();
  } catch(e) {
    // ignore
  }
}

async function submitOption4() {
  if (!confirm('Bạn có chắc chắn muốn nộp bài thi Kiểm tra chất lượng?')) return;
  const submitBtn = document.getElementById('submitBtnO4');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Đang chấm điểm...';

  const answers = collectO4Answers();

  try {
    const res = await fetch('/quiz/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        student_id: studentId,
        odd_answers: answers.odd_answers,
        even_answers: answers.even_answers
      })
    });
    const data = await res.json();
    if (!res.ok) {
      alert('Không thể nộp bài: ' + (data.detail || 'Lỗi hệ thống'));
      submitBtn.disabled = false;
      submitBtn.textContent = 'Nộp bài thi chất lượng';
      return;
    }

    localStorage.setItem('submitted_' + studentId, 'true');
    localStorage.setItem('results_' + studentId, JSON.stringify(data));

    showO4Results(data);
  } catch (err) {
    alert('Lỗi kết nối: ' + err.message);
    submitBtn.disabled = false;
    submitBtn.textContent = 'Nộp bài thi chất lượng';
  }
}

function showO4Results(data) {
  document.getElementById('screenOption4').classList.add('hidden');
  document.getElementById('screenResult').classList.remove('hidden');

  const oddMax = data.odd_max || 42;
  const evenMax = data.even_max || 42;
  const total = data.total || (oddMax + evenMax);

  const pct = Math.round((data.score / total) * 100);
  const emoji = pct === 100 ? '🏆' : pct >= 70 ? '🎉' : pct >= 40 ? '👍' : '💪';
  const title = pct === 100 ? 'Hoàn hảo!' : pct >= 70 ? 'Xuất sắc!' : pct >= 40 ? 'Khá tốt!' : 'Cố gắng hơn!';

  document.getElementById('resultEmoji').textContent = emoji;
  document.getElementById('resultTitle').textContent = title;
  document.getElementById('resultSub').textContent = `${studentName} – ${data.score}/${total} đúng (${pct}%)`;
  document.getElementById('scoreDisplay').textContent = `${data.score}/${total}`;

  const detail = document.getElementById('answerDetail');
  detail.innerHTML = `
    <div class="flex justify-between items-center py-1 border-b border-gray-100">
      <span class="font-semibold text-gray-700">Đề lẻ (1, 3, 5, 7)</span>
      <span class="font-bold text-blue-600">${data.odd_score}/${oddMax} điểm</span>
    </div>
    <div class="flex justify-between items-center py-1">
      <span class="font-semibold text-gray-700">Đề chẵn (2, 4, 6, 8)</span>
      <span class="font-bold text-blue-600">${data.even_score}/${evenMax} điểm</span>
    </div>
  `;
}
