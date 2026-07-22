let option5RoleOrder = [];

function escapeOption5(value) {
  const node = document.createElement('div');
  node.textContent = value || '';
  return node.innerHTML;
}

function initOption5() {
  const questions = document.getElementById('option5Questions');
  const roles = document.getElementById('option5Roles');
  if (!questions || !roles) return;
  option5RoleOrder = [...activeQuizSteps].sort(() => Math.random() - 0.5);
  questions.innerHTML = activeQuizSteps.map((step, index) => `
    <div class="bg-slate-800/80 border border-white/10 rounded-xl p-3">
      <label class="block text-sm font-bold text-white mb-2">${index + 1}. ${escapeOption5(step.left_text)}</label>
      <select data-category-id="${step.id}" class="option5-answer w-full bg-slate-950 border border-white/20 rounded-lg px-3 py-2 text-sm text-yellow-300 focus:outline-none focus:border-blue-500">
        <option value="">-- Chọn vai trò thích hợp --</option>
        ${option5RoleOrder.map((role, i) => `<option value="${role.id}">${String.fromCharCode(65 + i)}. ${escapeOption5(role.right_text)}</option>`).join('')}
      </select>
    </div>`).join('');
  roles.innerHTML = option5RoleOrder.map((role, i) => `<div class="bg-slate-800/80 border border-white/10 rounded-xl p-3 text-sm text-slate-200 flex gap-3"><span class="shrink-0 bg-blue-600/30 text-blue-300 font-black px-2 py-0.5 rounded">${String.fromCharCode(65 + i)}</span><span>${escapeOption5(role.right_text)}</span></div>`).join('');
}

async function submitOption5() {
  const selects = [...document.querySelectorAll('.option5-answer')];
  if (selects.some(select => !select.value) && !confirm('Bạn chưa ghép đủ 8 hạng mục. Vẫn nộp bài?')) return;
  if (!confirm('Xác nhận nộp bài kiểm tra?')) return;
  const button = document.getElementById('submitOption5Btn');
  button.disabled = true;
  const matchingAnswers = {};
  selects.forEach(select => { matchingAnswers[select.dataset.categoryId] = select.value; });
  try {
    const response = await fetch('/quiz/submit', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({student_id: studentId, matching_answers: matchingAnswers})});
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Không thể nộp bài');
    localStorage.setItem('submitted_' + studentId, 'true');
    localStorage.setItem('results_' + studentId, JSON.stringify({score: result.score, total: result.total}));
    showOption5Result(result);
  } catch (error) { alert(error.message); button.disabled = false; }
}

function showOption5Result(result) {
  document.getElementById('screenOption5').classList.add('hidden');
  document.getElementById('screenResult').classList.remove('hidden');
  document.getElementById('resultEmoji').textContent = result.score === result.total ? '🏆' : '📝';
  document.getElementById('resultTitle').textContent = result.score === result.total ? 'Hoàn hảo!' : 'Đã hoàn thành';
  document.getElementById('resultSub').textContent = `${studentName} – Kết quả bài kiểm tra hạng mục cơ bản`;
  document.getElementById('scoreDisplay').textContent = `${result.score}/${result.total}`;
  document.getElementById('answerDetail').innerHTML = '';
}
