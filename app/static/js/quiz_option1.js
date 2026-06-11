// ═══════════════════════════════════════════════════════
//  OPTION 1: GRID BUILDING & DRAG & CLICK LOGIC
// ═══════════════════════════════════════════════════════
let dO1Item = null;

function initOption1() {
  renderOption1Pools();
  renderOption1Grid();
  refreshGridAndPools();
}

function renderOption1Pools() {
  let startId, endId;
  if (currentPart === 1) {
    startId = 1; endId = 7;
  } else if (currentPart === 2) {
    startId = 8; endId = 15;
  } else {
    startId = 16; endId = 23;
  }

  const imgIds = [];
  for (let i = startId; i <= endId; i++) imgIds.push(i);
  const images = shuffle(imgIds.map(x => ({id: x, src: `/images/${x}.png`})));
  const lefts = shuffle(O1_TEXTS.left.slice(startId - 1, endId).map((x, i) => ({id: startId + i, text: x})));
  const rights = shuffle(O1_TEXTS.right.slice(startId - 1, endId).map((x, i) => ({id: startId + i, text: x})));
  const notes = shuffle(O1_TEXTS.note.slice(startId - 1, endId).map((x, i) => ({id: startId + i, text: x})));
  const reasons = shuffle(O1_TEXTS.reason.slice(startId - 1, endId).map((x, i) => ({id: startId + i, text: x})));

  // Render Images Pool
  const imgPool = document.getElementById('poolImages');
  imgPool.innerHTML = '';
  images.forEach(img => {
    const card = document.createElement('div');
    card.className = 'pool-card bg-slate-800 border border-white/10 rounded-xl overflow-hidden p-1 w-20 flex-shrink-0';
    card.dataset.id = img.id;
    card.dataset.type = 'image_id';
    card.draggable = true;
    card.innerHTML = `<img src="${img.src}" class="w-full aspect-[4/3] object-cover rounded-lg pointer-events-none" />`;
    setupCardEvents(card);
    imgPool.appendChild(card);
  });

  // Render Left Text Pool
  const leftPool = document.getElementById('poolLeft');
  leftPool.innerHTML = '';
  lefts.forEach(t => {
    const card = createTextCard(t.id, t.text, 'left_id');
    leftPool.appendChild(card);
  });

  // Render Right Text Pool
  const rightPool = document.getElementById('poolRight');
  rightPool.innerHTML = '';
  rights.forEach(t => {
    const card = createTextCard(t.id, t.text, 'right_id');
    rightPool.appendChild(card);
  });

  // Render Note Text Pool
  const notePool = document.getElementById('poolNote');
  notePool.innerHTML = '';
  notes.forEach(t => {
    const card = createTextCard(t.id, t.text, 'note_id');
    notePool.appendChild(card);
  });

  // Render Reason Text Pool
  const reasonPool = document.getElementById('poolReason');
  reasonPool.innerHTML = '';
  reasons.forEach(t => {
    const card = createTextCard(t.id, t.text, 'reason_id');
    reasonPool.appendChild(card);
  });
}

function createTextCard(id, text, type) {
  const card = document.createElement('div');
  card.className = 'pool-card bg-slate-800 border border-white/10 rounded-xl px-3 py-1.5 text-xs max-w-[200px] whitespace-normal flex-shrink-0';
  card.dataset.id = id;
  card.dataset.type = type;
  card.draggable = true;
  card.textContent = text.length > 55 ? text.substring(0, 52) + '...' : text;
  card.title = text;
  setupCardEvents(card);
  return card;
}

function setupCardEvents(card) {
  // Desktop Drag
  card.addEventListener('dragstart', onO1DragStart);
  card.addEventListener('dragend', onO1DragEnd);
  
  // Click support (highly touch-friendly)
  card.addEventListener('click', function(e) {
    e.stopPropagation();
    if (selectedPoolItem) {
      selectedPoolItem.classList.remove('selected');
    }
    if (selectedPoolItem === this) {
      selectedPoolItem = null;
    } else {
      selectedPoolItem = this;
      this.classList.add('selected');
    }
  });
}

function onO1DragStart(e) {
  dO1Item = this;
  this.classList.add('opacity-50');
  e.dataTransfer.setData('text/plain', this.dataset.id);
}

function onO1DragEnd() {
  this.classList.remove('opacity-50');
}

function renderOption1Grid() {
  let startIdx, endIdx;
  if (currentPart === 1) {
    startIdx = 0; endIdx = 6;
  } else if (currentPart === 2) {
    startIdx = 7; endIdx = 14;
  } else {
    startIdx = 15; endIdx = 22;
  }

  // 1. Render Desktop Table
  const tbody = document.getElementById('gridTableBody');
  tbody.innerHTML = '';

  for (let r = startIdx; r <= endIdx; r++) {
    const tr = document.createElement('tr');
    tr.className = 'hover:bg-white/5 transition';

    // Col 1: STT
    const tdStt = document.createElement('td');
    tdStt.className = 'p-3 font-bold text-slate-400 text-center';
    tdStt.textContent = r + 1;
    tr.appendChild(tdStt);

    // Col 2: Image Slot
    const tdImg = document.createElement('td');
    tdImg.className = 'p-3';
    tdImg.appendChild(createTableCell(r, 'image_id'));
    tr.appendChild(tdImg);

    // Col 3: Left Slot
    const tdLeft = document.createElement('td');
    tdLeft.className = 'p-3';
    tdLeft.appendChild(createTableCell(r, 'left_id'));
    tr.appendChild(tdLeft);

    // Col 4: Right Slot
    const tdRight = document.createElement('td');
    tdRight.className = 'p-3';
    tdRight.appendChild(createTableCell(r, 'right_id'));
    tr.appendChild(tdRight);

    // Col 5: Note Slot
    const tdNote = document.createElement('td');
    tdNote.className = 'p-3';
    tdNote.appendChild(createTableCell(r, 'note_id'));
    tr.appendChild(tdNote);

    // Col 6: Reason Slot
    const tdReason = document.createElement('td');
    tdReason.className = 'p-3';
    tdReason.appendChild(createTableCell(r, 'reason_id'));
    tr.appendChild(tdReason);

    tbody.appendChild(tr);
  }

  // 2. Render Mobile Cards
  const mobileContainer = document.getElementById('mobileCardsContainer');
  if (mobileContainer) {
    mobileContainer.innerHTML = '';
    for (let r = startIdx; r <= endIdx; r++) {
      const card = document.createElement('div');
      card.className = 'glass-card rounded-2xl border border-white/10 p-4 space-y-3';
      
      const header = document.createElement('div');
      header.className = 'flex items-center justify-between border-b border-white/10 pb-1.5 mb-2';
      header.innerHTML = `
        <span class="text-xs font-black text-yellow-300">BƯỚC ${r + 1}</span>
      `;
      card.appendChild(header);

      const cols = [
        { name: 'image_id', label: '📸 Hình minh họa' },
        { name: 'left_id', label: '👈 Thao tác tay trái' },
        { name: 'right_id', label: '👉 Thao tác tay phải' },
        { name: 'note_id', label: '⚠️ Chú ý quan trọng' },
        { name: 'reason_id', label: '💡 Lý do thực hiện' }
      ];

      cols.forEach(col => {
        const itemWrapper = document.createElement('div');
        itemWrapper.className = 'space-y-1';
        
        const label = document.createElement('span');
        label.className = 'text-[10px] font-bold text-slate-400 uppercase tracking-wider block';
        label.textContent = col.label;
        itemWrapper.appendChild(label);

        const cell = createTableCell(r, col.name);
        itemWrapper.appendChild(cell);
        card.appendChild(itemWrapper);
      });

      mobileContainer.appendChild(card);
    }
  }
}

function createTableCell(rowIdx, colName) {
  const cell = document.createElement('div');
  cell.className = 'drop-cell border-2 border-dashed border-white/10 rounded-2xl flex items-center justify-center p-3 text-center text-xs text-white/30 italic hover:border-slate-500 transition cursor-pointer min-h-[50px]';
  cell.dataset.row = rowIdx;
  cell.dataset.col = colName;
  cell.textContent = colName === 'image_id' ? 'Chọn hình ảnh...' : 'Chọn ô chữ...';

  // Drag listeners
  cell.addEventListener('dragover', function(e) {
    e.preventDefault();
    if (dO1Item && dO1Item.dataset.type === colName) {
      this.classList.add('over');
    }
  });
  cell.addEventListener('dragleave', function() {
    this.classList.remove('over');
  });
  cell.addEventListener('drop', function(e) {
    e.preventDefault();
    this.classList.remove('over');
    if (dO1Item && dO1Item.dataset.type === colName) {
      placeItem(parseInt(dO1Item.dataset.id), rowIdx, colName);
    }
  });

  // Click to place
  cell.addEventListener('click', function(e) {
    e.stopPropagation();
    openSelectionModal(rowIdx, colName);
  });

  return cell;
}

function placeItem(id, row, col) {
  // First, check if this ID is already placed elsewhere in this column. If so, clear it.
  for (let r = 0; r < 23; r++) {
    if (gridPlacement[r][col] === id) {
      gridPlacement[r][col] = null;
    }
  }

  // Set the value
  gridPlacement[row][col] = id;
  localStorage.setItem('gridPlacement_' + studentId, JSON.stringify(gridPlacement));

  // Render changes
  refreshGridAndPools();
}

function removeItem(row, col) {
  gridPlacement[row][col] = null;
  localStorage.setItem('gridPlacement_' + studentId, JSON.stringify(gridPlacement));
  refreshGridAndPools();
}

function refreshGridAndPools() {
  // Find which IDs are used in each column
  const used = {
    image_id: new Set(),
    left_id: new Set(),
    right_id: new Set(),
    note_id: new Set(),
    reason_id: new Set()
  };

  for (let r = 0; r < 23; r++) {
    for (const key in used) {
      if (gridPlacement[r][key] !== null) {
        used[key].add(gridPlacement[r][key]);
      }
    }
  }

  // Update Pool items visibility
  document.querySelectorAll('.pool-card').forEach(card => {
    const id = parseInt(card.dataset.id);
    const type = card.dataset.type;
    if (used[type].has(id)) {
      card.classList.add('hidden');
    } else {
      card.classList.remove('hidden');
    }
  });

  // Update Cells content
  document.querySelectorAll('.drop-cell').forEach(cell => {
    const row = parseInt(cell.dataset.row);
    const col = cell.dataset.col;
    const val = gridPlacement[row][col];

    cell.className = 'drop-cell border rounded-2xl flex items-center justify-center p-3 text-center text-xs transition cursor-pointer';
    cell.innerHTML = '';

    if (val === null) {
      cell.classList.add('border-dashed', 'border-white/10', 'text-white/30', 'italic', 'hover:border-slate-500');
      cell.textContent = col === 'image_id' ? 'Chọn hình ảnh...' : 'Chọn ô chữ...';
    } else {
      cell.classList.add('border-solid', 'border-blue-500/50', 'bg-blue-950/40', 'text-white');
      if (col === 'image_id') {
        cell.innerHTML = `<img src="/images/${val}.png" class="w-full aspect-[4/3] object-cover rounded-lg" />`;
      } else {
        let text = '';
        if (col === 'left_id') text = O1_TEXTS.left[val - 1];
        else if (col === 'right_id') text = O1_TEXTS.right[val - 1];
        else if (col === 'note_id') text = O1_TEXTS.note[val - 1];
        else if (col === 'reason_id') text = O1_TEXTS.reason[val - 1];
        cell.textContent = text;
      }
    }
  });

  updateOption1Progress();
}

function openSelectionModal(rowIdx, colName) {
  const modal = document.getElementById('selectionModal');
  const title = document.getElementById('selectionTitle');
  const optionsDiv = document.getElementById('selectionOptions');
  const actionsDiv = document.getElementById('selectionActions');
  const btnRemove = document.getElementById('btnRemoveSelection');

  let colLabel = '';
  if (colName === 'image_id') colLabel = 'Hình minh họa';
  else if (colName === 'left_id') colLabel = 'Thao tác tay trái';
  else if (colName === 'right_id') colLabel = 'Thao tác tay phải';
  else if (colName === 'note_id') colLabel = 'Chú ý quan trọng';
  else if (colName === 'reason_id') colLabel = 'Lý do thực hiện';

  title.textContent = `Chọn ${colLabel} - Bước ${rowIdx + 1}`;

  const usedIds = new Set();
  for (let r = 0; r < 23; r++) {
    if (r !== rowIdx && gridPlacement[r][colName] !== null) {
      usedIds.add(gridPlacement[r][colName]);
    }
  }

  optionsDiv.innerHTML = '';
  const currentVal = gridPlacement[rowIdx][colName];

  let startId, endId;
  if (currentPart === 1) {
    startId = 1; endId = 7;
  } else if (currentPart === 2) {
    startId = 8; endId = 15;
  } else {
    startId = 16; endId = 23;
  }

  let availableItems = [];
  if (colName === 'image_id') {
    for (let id = startId; id <= endId; id++) {
      if (!usedIds.has(id)) {
        availableItems.push({ id, src: `/images/${id}.png` });
      }
    }
  } else {
    let textArr = [];
    if (colName === 'left_id') textArr = O1_TEXTS.left;
    else if (colName === 'right_id') textArr = O1_TEXTS.right;
    else if (colName === 'note_id') textArr = O1_TEXTS.note;
    else if (colName === 'reason_id') textArr = O1_TEXTS.reason;

    textArr.forEach((text, i) => {
      const id = i + 1;
      if (id >= startId && id <= endId && !usedIds.has(id)) {
        availableItems.push({ id, text });
      }
    });
  }

  // Shuffle options to randomize order in selection drawer
  availableItems = shuffle(availableItems);

  if (availableItems.length === 0) {
    optionsDiv.innerHTML = `<p class="text-xs text-slate-400 italic text-center py-4">Không còn mảnh ghép nào sẵn có.</p>`;
  } else {
    availableItems.forEach((item, index) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'w-full text-left bg-slate-800 hover:bg-slate-700/80 border border-white/10 rounded-xl p-3 text-xs text-slate-200 transition active:scale-[0.99] flex items-center gap-3 font-medium';
      
      const isCurrent = (currentVal === item.id);
      if (isCurrent) {
        btn.classList.add('border-blue-500', 'bg-blue-950/40', 'text-white');
      }

      if (colName === 'image_id') {
        btn.innerHTML = `
          <img src="${item.src}" class="w-16 aspect-[4/3] object-cover rounded-lg border border-white/5" />
          <span class="text-xs text-slate-400">Hình ảnh ${index + 1}</span>
          ${isCurrent ? '<span class="ml-auto text-blue-400 font-bold text-sm">✓</span>' : ''}
        `;
      } else {
        btn.innerHTML = `
          <span class="flex-1">${item.text}</span>
          ${isCurrent ? '<span class="ml-auto text-blue-400 font-bold text-sm">✓</span>' : ''}
        `;
      }

      btn.addEventListener('click', () => {
        placeItem(item.id, rowIdx, colName);
        closeSelectionModal();
      });

      optionsDiv.appendChild(btn);
    });
  }

  if (currentVal !== null) {
    actionsDiv.classList.remove('hidden');
    btnRemove.onclick = () => {
      removeItem(rowIdx, colName);
      closeSelectionModal();
    };
  } else {
    actionsDiv.classList.add('hidden');
  }

  modal.classList.remove('hidden');
}

function closeSelectionModal() {
  document.getElementById('selectionModal').classList.add('hidden');
}

function updateOption1Progress() {
  let filled = 0;
  for (let r = 0; r < 23; r++) {
    for (const key in gridPlacement[r]) {
      if (gridPlacement[r][key] !== null) filled++;
    }
  }
  document.getElementById('progressTextO1').textContent = `Đã xếp: ${filled}/115 ô (Phần ${currentPart}/3)`;
  
  const btnPrev = document.getElementById('prevBtnO1');
  const btnNext = document.getElementById('nextBtnO1');
  const btnSubmit = document.getElementById('submitBtnO1');
  
  if (btnPrev) btnPrev.disabled = (currentPart === 1);
  if (btnNext) {
    if (currentPart === 3) {
      btnNext.textContent = 'Hoàn thành';
    } else {
      btnNext.textContent = 'Tiếp';
    }
  }
  if (btnSubmit) {
    btnSubmit.disabled = (currentPart !== 3);
  }
}

function goToPrevPart() {
  if (currentPart > 1) {
    currentPart--;
    initOption1();
  }
}

function goToNextPart() {
  if (currentPart < 3) {
    currentPart++;
    initOption1();
  } else {
    triggerSubmitFlow();
  }
}

function triggerSubmitFlow() {
  let filled = 0;
  for (let r = 0; r < 23; r++) {
    for (const key in gridPlacement[r]) {
      if (gridPlacement[r][key] !== null) filled++;
    }
  }

  if (filled < 115) {
    if (confirm(`Bạn chưa hoàn thành hết bài thi (chỉ mới xếp được ${filled}/115 ô). Bạn có chắc chắn muốn nộp bài không?`)) {
      if (confirm('Xác nhận nộp bài? Nhấn OK để gửi kết quả bài thi.')) {
        submitQuizOption1();
      }
    }
  } else {
    if (confirm('Bạn đã hoàn thành toàn bộ bài thi. Xác nhận nộp bài?')) {
      submitQuizOption1();
    }
  }
}

async function submitQuizOption1() {
  const filled = 35;
  const btn = document.getElementById('submitBtnO1');
  btn.disabled = true;
  btn.textContent = 'Đang nộp...';

  // Format payload: list of row configurations
  const answerOrder = gridPlacement.map((row, i) => ({
    row_idx: i,
    image_id: row.image_id,
    left_id: row.left_id,
    right_id: row.right_id,
    note_id: row.note_id,
    reason_id: row.reason_id
  }));

  try {
    const res = await fetch('/quiz/submit', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ student_id: studentId, answer_order: answerOrder })
    });
    const data = await res.json();
    if (!res.ok) {
      alert('Lỗi nộp bài.');
      btn.disabled = false;
      return;
    }

    localStorage.setItem('submitted_' + studentId, 'true');
    localStorage.setItem('results_' + studentId, JSON.stringify(data));

    showO1Results(data);
  } catch (err) {
    alert('Lỗi kết nối.');
    btn.disabled = false;
  }
}

function showO1Results(data) {
  document.getElementById('screenOption1').classList.add('hidden');
  document.getElementById('screenResult').classList.remove('hidden');

  const pct = Math.round(data.score / 23 * 100);
  const emoji = pct === 100 ? '🏆' : pct >= 70 ? '🎉' : pct >= 40 ? '👍' : '💪';
  const title = pct === 100 ? 'Hoàn hảo!' : pct >= 70 ? 'Xuất sắc!' : pct >= 40 ? 'Khá tốt!' : 'Cố gắng hơn!';

  document.getElementById('resultEmoji').textContent = emoji;
  document.getElementById('resultTitle').textContent = title;
  document.getElementById('resultSub').textContent = `${studentName} – ${data.score}/23 đúng (${pct}%)`;
  document.getElementById('scoreDisplay').textContent = `${data.score}/23`;

  const detail = document.getElementById('answerDetail');
  detail.innerHTML = '';

  for (let r = 0; r < 23; r++) {
    const row = gridPlacement[r];
    const step_num = r + 1;
    const correct_img = step_num;
    const correct_left = step_num;
    const correct_right = step_num;
    const correct_note = step_num;
    const correct_reason = step_num;

    const ok = (row.image_id === correct_img && 
                row.left_id && O1_TEXTS.left[row.left_id - 1] === O1_TEXTS.left[correct_left - 1] && 
                row.right_id && O1_TEXTS.right[row.right_id - 1] === O1_TEXTS.right[correct_right - 1] && 
                row.note_id && O1_TEXTS.note[row.note_id - 1] === O1_TEXTS.note[correct_note - 1] && 
                row.reason_id && O1_TEXTS.reason[row.reason_id - 1] === O1_TEXTS.reason[correct_reason - 1]);

    const div = document.createElement('div');
    div.className = `p-2.5 rounded-xl text-xs ${ok ? 'bg-green-50 border border-green-200 text-green-800' : 'bg-red-50 border border-red-200 text-red-800'}`;
    div.innerHTML = `
      <div class="flex items-center gap-1.5 font-bold">
        <span>${ok ? '✅' : '❌'}</span>
        <span>Dòng ${r+1}:</span>
        <span class="${ok ? 'text-green-700' : 'text-red-700'}">${ok ? 'ĐÚNG HOÀN TOÀN' : 'CÓ LỖI SAI'}</span>
      </div>`;
    detail.appendChild(div);
  }
}
