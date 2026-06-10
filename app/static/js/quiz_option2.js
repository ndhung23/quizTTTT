// ═══════════════════════════════════════════════════════
//  OPTION 2: TIE SUB-QUIZZES MANAGER
// ═══════════════════════════════════════════════════════
const SUB_QUIZ_MAX_SCORES = {
  1: 5,
  2: 7,
  3: 5,
  4: 5,
  5: 9,
  6: 2,
  7: 4,
  8: 4,
  9: 5,
  10: 4
};

function loadOption2State() {
  updateOption2Dashboard();
}

function updateOption2Dashboard() {
  let accumulated = 0;
  for (let id = 1; id <= 10; id++) {
    const btn = document.getElementById(`subBtn-${id}`);
    const scoreText = document.getElementById(`subScore-${id}`);
    const statusText = document.getElementById(`subStatus-${id}`);

    if (completedSubQuizzes.includes(id)) {
      btn.className = 'sub-card-green rounded-2xl p-5 text-left transition hover:scale-[1.02] flex flex-col justify-between h-36';
      statusText.textContent = 'Đã nộp';
      statusText.className = 'text-xs text-green-700 font-bold';
      
      const score = subQuizScores[id] || 0;
      const maxScore = SUB_QUIZ_MAX_SCORES[id];
      scoreText.textContent = `${score}/${maxScore} đ`;
      accumulated += score;
    } else {
      btn.className = 'sub-card-white rounded-2xl p-5 text-left transition hover:scale-[1.02] flex flex-col justify-between h-36';
      statusText.textContent = 'Chưa làm';
      statusText.className = 'text-xs text-slate-500 font-semibold';
      scoreText.textContent = '';
    }
  }
  document.getElementById('totalScoreO2').textContent = accumulated;
  const progressText = document.getElementById('progressTextO2');
  if (progressText) {
    progressText.textContent = `Đã làm: ${completedSubQuizzes.length}/10 bài`;
  }
}

function openSubQuiz(id) {
  activeSubQuizId = id;
  const quiz = SUB_QUIZ_DATA[id];
  document.getElementById('modalTitle').textContent = quiz.title;
  
  const content = document.getElementById('modalContent');
  content.innerHTML = '';
  
  if (quiz.type === 'matching') {
    renderMatchingExercise(quiz);
  } else if (quiz.type === 'fill') {
    renderFillExercise(quiz);
  } else if (quiz.type === 'tf') {
    renderTfExercise(quiz);
  } else if (quiz.type === 'single_choice_image') {
    renderSingleChoiceImageExercise(quiz);
  } else if (quiz.type === 'custom_inputs_image') {
    renderCustomInputsImageExercise(quiz);
  }

  // Pre-fill if already completed
  if (completedSubQuizzes.includes(id)) {
    document.getElementById('modalSubmitBtn').disabled = true;
    document.getElementById('modalSubmitBtn').textContent = 'Đã nộp bài';
  } else {
    document.getElementById('modalSubmitBtn').disabled = false;
    document.getElementById('modalSubmitBtn').textContent = 'Lưu bài làm';
  }

  document.getElementById('subQuizModal').classList.remove('hidden');
}

function closeSubQuizModal() {
  document.getElementById('subQuizModal').classList.add('hidden');
  activeSubQuizId = null;
}

// ── RENDER SUB QUIZ EXERCISES ──────────────────────────────────
// 1. Matching UI: Dropdown matching picker modal
function renderMatchingExercise(quiz) {
  const container = document.createElement('div');
  container.className = 'space-y-4';

  const desc = document.createElement('p');
  desc.className = 'text-xs text-yellow-400 font-semibold uppercase tracking-wider';
  desc.textContent = 'Ghép các thuật ngữ bên trái với giải thích phù hợp bên phải:';
  container.appendChild(desc);

  // Grouped structure
  const grid = document.createElement('div');
  grid.className = 'grid grid-cols-1 md:grid-cols-2 gap-4';

  const leftDiv = document.createElement('div');
  leftDiv.className = 'space-y-3';
  
  quiz.left.forEach((term, idx) => {
    const item = document.createElement('div');
    item.className = 'bg-slate-800 border border-white/10 rounded-xl p-3.5 flex flex-col gap-2 shadow-sm';
    
    const title = document.createElement('div');
    title.className = 'font-bold text-sm text-blue-400';
    title.textContent = `${idx + 1}. ${term}`;
    item.appendChild(title);

    // Hidden input to store selected value for grading compatibility
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.className = 'sub-quiz-input';
    hiddenInput.dataset.leftIdx = idx;
    hiddenInput.value = '';
    item.appendChild(hiddenInput);

    // Trigger button
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'sub-quiz-trigger bg-slate-900 border border-white/20 hover:border-slate-500 rounded-lg p-2.5 text-xs focus:outline-none focus:border-blue-500 w-full font-medium text-slate-400 text-left transition flex items-center justify-between';
    btn.innerHTML = `<span>Chọn định nghĩa thích hợp...</span>
                     <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                       <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                     </svg>`;
    
    btn.addEventListener('click', () => {
      openMatchingPicker(quiz, idx, hiddenInput, btn);
    });

    item.appendChild(btn);
    leftDiv.appendChild(item);
  });

  const rightDiv = document.createElement('div');
  rightDiv.className = 'space-y-2 bg-slate-900/60 rounded-2xl p-4 border border-white/5';
  
  const rightTitle = document.createElement('h4');
  rightTitle.className = 'text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-white/10 pb-2 mb-2';
  rightTitle.textContent = 'Danh sách các giải thích / vai trò';
  rightDiv.appendChild(rightTitle);

  quiz.right.forEach(def => {
    const card = document.createElement('div');
    card.className = 'bg-slate-800/80 rounded-lg p-3 text-xs border border-white/5 flex gap-2';
    card.innerHTML = `<span class="bg-blue-600/30 text-blue-300 font-bold px-2 py-0.5 rounded h-fit">${def.id}</span>
                      <span class="text-slate-300 font-medium">${def.text}</span>`;
    rightDiv.appendChild(card);
  });

  grid.appendChild(leftDiv);
  grid.appendChild(rightDiv);
  container.appendChild(grid);
  document.getElementById('modalContent').appendChild(container);
}

function openMatchingPicker(quiz, leftIdx, hiddenInput, triggerBtn) {
  const modal = document.getElementById('matchingPickerModal');
  const title = document.getElementById('matchingPickerTitle');
  const optionsDiv = document.getElementById('matchingPickerOptions');

  const termText = quiz.left[leftIdx];
  title.textContent = `Ghép thuật ngữ: "${termText}"`;

  optionsDiv.innerHTML = '';

  // Shuffle right options to randomize definition order in picker modal
  shuffle(quiz.right).forEach(def => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'w-full text-left bg-slate-800 hover:bg-slate-700/80 border border-white/10 rounded-xl p-3 text-xs text-slate-200 transition active:scale-[0.99] flex gap-3 font-medium';
    
    const isCurrent = (hiddenInput.value === def.id);
    if (isCurrent) {
      btn.classList.add('border-blue-500', 'bg-blue-950/40', 'text-white');
    }

    btn.innerHTML = `
      <span class="shrink-0 bg-blue-600/30 text-blue-300 font-bold px-2 py-0.5 rounded h-fit">${def.id}</span>
      <span class="flex-1">${def.text}</span>
      ${isCurrent ? '<span class="ml-auto text-blue-400 font-bold text-sm">✓</span>' : ''}
    `;

    btn.addEventListener('click', () => {
      hiddenInput.value = def.id;
      triggerBtn.classList.remove('text-slate-400');
      triggerBtn.classList.add('text-yellow-400', 'border-blue-500/50');
      triggerBtn.querySelector('span').textContent = `(${def.id}) ${def.text}`;
      closeMatchingPicker();
    });

    optionsDiv.appendChild(btn);
  });

  modal.classList.remove('hidden');
}

function closeMatchingPicker() {
  document.getElementById('matchingPickerModal').classList.add('hidden');
}

// 2. Fill in the blanks UI
function renderFillExercise(quiz) {
  const container = document.createElement('div');
  container.className = 'space-y-6 p-4';

  const desc = document.createElement('p');
  desc.className = 'text-xs text-yellow-400 font-semibold uppercase tracking-wider';
  desc.textContent = 'Chọn từ thích hợp từ danh sách rồi điền vào các khoảng trống (C) và (A):';
  container.appendChild(desc);

  // Styled Paragraph with inline select boxes
  const textDiv = document.createElement('div');
  textDiv.className = 'bg-slate-900/80 rounded-2xl p-6 border border-white/10 text-base leading-loose font-medium text-slate-200';
  
  // Replace {0} and {1} with inputs
  let formattedText = quiz.text;
  
  const select0 = `<select class="sub-quiz-input bg-slate-800 border border-blue-500/50 rounded-lg px-2.5 py-1 text-sm inline-block mx-1 focus:outline-none focus:ring-1 focus:ring-blue-500 font-bold text-yellow-300" data-blank-idx="0">
    <option value="">(Chọn từ)</option>
    ${quiz.options.map(opt => `<option value="${opt}">${opt}</option>`).join('')}
  </select>`;
  
  const select1 = `<select class="sub-quiz-input bg-slate-800 border border-blue-500/50 rounded-lg px-2.5 py-1 text-sm inline-block mx-1 focus:outline-none focus:ring-1 focus:ring-blue-500 font-bold text-yellow-300" data-blank-idx="1">
    <option value="">(Chọn từ)</option>
    ${quiz.options.map(opt => `<option value="${opt}">${opt}</option>`).join('')}
  </select>`;

  formattedText = formattedText.replace('{0}', select0).replace('{1}', select1);
  textDiv.innerHTML = formattedText;
  container.appendChild(textDiv);

  document.getElementById('modalContent').appendChild(container);
}

// 3. True / False and Dropdown items selection (Quiz 9 & 10)
function renderTfExercise(quiz) {
  const container = document.createElement('div');
  container.className = 'space-y-4';

  const desc = document.createElement('p');
  desc.className = 'text-xs text-yellow-400 font-semibold uppercase tracking-wider';
  desc.textContent = 'Lựa chọn đáp án chính xác cho từng câu hỏi bên dưới:';
  container.appendChild(desc);

  quiz.questions.forEach((q, idx) => {
    const item = document.createElement('div');
    item.className = 'bg-slate-900/60 border border-white/5 rounded-2xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-3';
    
    const text = document.createElement('div');
    text.className = 'text-sm font-semibold text-slate-200';
    text.textContent = `${idx + 1}. ${q.text}`;
    item.appendChild(text);

    const inputContainer = document.createElement('div');
    
    if (quiz.type === 'tf' && !quiz.options) {
      // True/False (O/X) Radio select
      inputContainer.className = 'flex gap-2 shrink-0';
      inputContainer.innerHTML = `
        <label class="flex items-center gap-1.5 cursor-pointer bg-slate-800 hover:bg-slate-700/80 px-3.5 py-2 rounded-xl transition">
          <input type="radio" name="tf-${q.id}" value="O" class="sub-quiz-input" data-question-id="${q.id}">
          <span class="text-sm font-bold text-green-400">O (Đúng)</span>
        </label>
        <label class="flex items-center gap-1.5 cursor-pointer bg-slate-800 hover:bg-slate-700/80 px-3.5 py-2 rounded-xl transition">
          <input type="radio" name="tf-${q.id}" value="X" class="sub-quiz-input" data-question-id="${q.id}">
          <span class="text-sm font-bold text-red-400">X (Sai)</span>
        </label>
      `;
    } else {
      // Dropdown options
      const select = document.createElement('select');
      select.className = 'sub-quiz-input bg-slate-800 border border-white/20 rounded-xl px-4 py-2 text-xs focus:outline-none focus:border-blue-500 w-48 font-bold text-yellow-300';
      select.dataset.questionId = q.id;

      const optDefault = document.createElement('option');
      optDefault.value = '';
      optDefault.textContent = '--- Chọn đáp án ---';
      select.appendChild(optDefault);

      quiz.options.forEach(opt => {
        const o = document.createElement('option');
        o.value = opt;
        o.textContent = opt;
        select.appendChild(o);
      });
      inputContainer.appendChild(select);
    }

    item.appendChild(inputContainer);
    container.appendChild(item);
  });

  document.getElementById('modalContent').appendChild(container);
}

function renderSingleChoiceImageExercise(quiz) {
  const container = document.createElement('div');
  container.className = 'space-y-4';

  const img = document.createElement('img');
  img.src = quiz.image;
  img.className = 'w-full max-h-96 object-contain rounded-xl border border-white/10 shadow mx-auto';
  container.appendChild(img);

  const desc = document.createElement('p');
  desc.className = 'text-xs text-yellow-400 font-semibold uppercase tracking-wider';
  desc.textContent = 'Chọn đáp án đúng:';
  container.appendChild(desc);

  const optionsDiv = document.createElement('div');
  optionsDiv.className = 'grid grid-cols-2 gap-3';

  quiz.options.forEach((opt, idx) => {
    const label = document.createElement('label');
    label.className = 'flex items-center gap-3 cursor-pointer bg-slate-800 hover:bg-slate-700/80 border border-white/10 p-3.5 rounded-xl transition active:scale-[0.99]';
    
    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.name = `q7-option`;
    radio.value = opt;
    radio.className = 'sub-quiz-input w-4 h-4 text-blue-600 focus:ring-blue-500 border-white/10 bg-slate-900';
    
    const span = document.createElement('span');
    span.className = 'text-sm font-semibold text-slate-200';
    span.textContent = opt;

    label.appendChild(radio);
    label.appendChild(span);
    optionsDiv.appendChild(label);
  });

  container.appendChild(optionsDiv);
  document.getElementById('modalContent').appendChild(container);
}

function renderCustomInputsImageExercise(quiz) {
  const container = document.createElement('div');
  container.className = 'space-y-4';

  const img = document.createElement('img');
  img.src = quiz.image;
  img.className = 'w-full max-h-[450px] object-contain rounded-xl border border-white/10 shadow mx-auto';
  container.appendChild(img);

  const desc = document.createElement('p');
  desc.className = 'text-xs text-yellow-400 font-semibold uppercase tracking-wider';
  desc.textContent = 'Nhập số thích hợp vào các ô A, B, C, D:';
  container.appendChild(desc);

  const inputsDiv = document.createElement('div');
  inputsDiv.className = 'grid grid-cols-2 gap-4';

  quiz.inputs.forEach(key => {
    const item = document.createElement('div');
    item.className = 'bg-slate-800 border border-white/10 rounded-xl p-3 flex items-center justify-between gap-3';
    
    const label = document.createElement('span');
    label.className = 'text-sm font-bold text-blue-400';
    label.textContent = `Ô ${key}:`;
    
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'sub-quiz-input bg-slate-900 border border-white/20 hover:border-slate-500 rounded-lg p-2 text-center text-sm font-bold text-yellow-300 focus:outline-none focus:border-blue-500 w-24';
    input.dataset.key = key;
    input.placeholder = 'Nhập số...';
    
    item.appendChild(label);
    item.appendChild(input);
    inputsDiv.appendChild(item);
  });

  container.appendChild(inputsDiv);
  document.getElementById('modalContent').appendChild(container);
}

// ── GRADE AND SUBMIT SUB QUIZ ──────────────────────────────────
async function gradeAndSubmitSubQuiz() {
  const id = activeSubQuizId;
  if (!id) return;
  const quiz = SUB_QUIZ_DATA[id];
  
  let score = 0;
  let allAnswered = true;

  if (quiz.type === 'matching') {
    const selects = document.querySelectorAll('.sub-quiz-input');
    selects.forEach(select => {
      const leftIdx = select.dataset.leftIdx;
      const answer = select.value;
      if (!answer) allAnswered = false;
      if (quiz.correct[leftIdx] === answer) {
        score++;
      }
    });
  } else if (quiz.type === 'fill') {
    const selects = document.querySelectorAll('.sub-quiz-input');
    selects.forEach(select => {
      const blankIdx = select.dataset.blankIdx;
      const answer = select.value;
      if (!answer) allAnswered = false;
      if (quiz.correct[blankIdx] === answer) {
        score++;
      }
    });
  } else if (quiz.type === 'tf') {
    if (!quiz.options) {
      // Radio group checking
      const questions = quiz.questions;
      questions.forEach(q => {
        const selected = document.querySelector(`input[name="tf-${q.id}"]:checked`);
        if (!selected) {
          allAnswered = false;
        } else {
          const val = selected.value;
          if (quiz.correct[q.id] === val) {
            score++;
          }
        }
      });
    } else {
      // Dropdown select checking
      const selects = document.querySelectorAll('.sub-quiz-input');
      selects.forEach(select => {
        const qId = select.dataset.questionId;
        const answer = select.value;
        if (!answer) allAnswered = false;
        if (quiz.correct[qId] === answer) {
          score++;
        }
      });
    }
  } else if (quiz.type === 'single_choice_image') {
    const selected = document.querySelector(`input[name="q7-option"]:checked`);
    if (!selected) {
      allAnswered = false;
    } else {
      const val = selected.value;
      if (quiz.correct[0] === val) {
        score = 4;
      }
    }
  } else if (quiz.type === 'custom_inputs_image') {
    const inputs = document.querySelectorAll('.sub-quiz-input');
    inputs.forEach(input => {
      const key = input.dataset.key;
      const answer = input.value.trim();
      if (!answer) allAnswered = false;
      if (quiz.correct[key] === answer) {
        score++;
      }
    });
  }

  if (!allAnswered) {
    if (!confirm('Bạn chưa hoàn thành tất cả các câu hỏi trong bài này. Vẫn nộp?')) {
      return;
    }
  }

  // Submit to server
  const btn = document.getElementById('modalSubmitBtn');
  btn.disabled = true;
  btn.textContent = 'Đang lưu...';

  try {
    const res = await fetch('/quiz/submit', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        student_id: studentId,
        sub_quiz_id: id,
        sub_score: score
      })
    });
    const data = await res.json();
    if (!res.ok) {
      alert('Gặp lỗi lưu bài.');
      btn.disabled = false;
      btn.textContent = 'Lưu bài làm';
      return;
    }

    // Update local state
    if (!completedSubQuizzes.includes(id)) {
      completedSubQuizzes.push(id);
    }
    subQuizScores[id] = score;

    // Save to localStorage
    localStorage.setItem('completedSubQuizzes_' + studentId, JSON.stringify(completedSubQuizzes));
    localStorage.setItem('subQuizScores_' + studentId, JSON.stringify(subQuizScores));

    updateOption2Dashboard();
    closeSubQuizModal();

    // Check if all 10 are completed, show congratulations
    if (completedSubQuizzes.length === 10) {
      showO2FinalResult(data.score, data.total);
      
      // Save final Option 2 submission results
      localStorage.setItem('submitted_' + studentId, 'true');
      localStorage.setItem('results_' + studentId, JSON.stringify({ score: data.score, total: data.total }));
    }

  } catch {
    alert('Lỗi kết nối mạng.');
    btn.disabled = false;
    btn.textContent = 'Lưu bài làm';
  }
}

function showO2FinalResult(totalScore, maxScore) {
  document.getElementById('screenOption2').classList.add('hidden');
  document.getElementById('screenResult').classList.remove('hidden');

  const pct = Math.round(totalScore / maxScore * 100);
  const emoji = pct === 100 ? '🏆' : pct >= 70 ? '🎉' : pct >= 40 ? '👍' : '💪';
  const title = pct === 100 ? 'Hoàn hảo!' : pct >= 70 ? 'Xuất sắc!' : pct >= 40 ? 'Khá tốt!' : 'Cố gắng hơn!';

  document.getElementById('resultEmoji').textContent = emoji;
  document.getElementById('resultTitle').textContent = title;
  document.getElementById('resultSub').textContent = `${studentName} – Bạn đã hoàn thành toàn bộ 10 bài kiểm tra TIE!`;
  document.getElementById('scoreDisplay').textContent = `${totalScore}/${maxScore}`;

  const detail = document.getElementById('answerDetail');
  detail.innerHTML = '';

  for (let id = 1; id <= 10; id++) {
    const quizTitle = SUB_QUIZ_DATA[id].title;
    const score = subQuizScores[id] || 0;
    const max = SUB_QUIZ_MAX_SCORES[id];

    const div = document.createElement('div');
    div.className = 'p-2 rounded-lg text-xs bg-slate-100 flex items-center justify-between text-slate-700 font-semibold';
    div.innerHTML = `<span>${quizTitle}</span><span class="text-blue-600 font-bold">${score}/${max} đ</span>`;
    detail.appendChild(div);
  }
}

function triggerSubmitFlowO2() {
  const count = completedSubQuizzes.length;
  if (count < 10) {
    if (confirm(`Bạn chưa hoàn thành hết 10 bài kiểm tra (chỉ mới làm ${count}/10 bài). Bạn có chắc chắn muốn nộp bài thi không?`)) {
      if (confirm('Xác nhận nộp bài? Kết quả của bạn sẽ được chốt và chấm điểm ngay lập tức.')) {
        submitQuizOption2Final();
      }
    }
  } else {
    if (confirm('Bạn đã hoàn thành toàn bộ 10 bài kiểm tra. Xác nhận nộp bài?')) {
      submitQuizOption2Final();
    }
  }
}

function submitQuizOption2Final() {
  const totalScore = parseInt(document.getElementById('totalScoreO2').textContent) || 0;
  
  localStorage.setItem('submitted_' + studentId, 'true');
  localStorage.setItem('results_' + studentId, JSON.stringify({ score: totalScore, total: 50 }));

  showO2FinalResult(totalScore, 50);
}
