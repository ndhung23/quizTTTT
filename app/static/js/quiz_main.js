// ═══════════════════════════════════════════════════════
//  AUTO-FILL ROOM CODE FROM URL
// ═══════════════════════════════════════════════════════
const _code = new URLSearchParams(location.search).get('code');
if (_code) {
  const codeInput = document.getElementById('codeInput');
  if (codeInput) codeInput.value = _code.toUpperCase();
}

// ═══════════════════════════════════════════════════════
//  SCREEN 1: JOIN LOGIC
// ═══════════════════════════════════════════════════════
const joinForm = document.getElementById('joinForm');
if (joinForm) {
  joinForm.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = document.getElementById('joinBtn');
    const spinner = document.getElementById('joinSpinner');
    const errEl = document.getElementById('joinError');
    btn.disabled = true;
    spinner.classList.remove('hidden');
    errEl.classList.add('hidden');

    const code = document.getElementById('codeInput').value.trim().toUpperCase();
    const name = document.getElementById('nameInput').value.trim();

    try {
      const res = await fetch('/quiz/join', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, code })
      });
      const data = await res.json();
      if (!res.ok) {
        errEl.textContent = data.detail || 'Mã không hợp lệ hoặc đã hết hạn';
        errEl.classList.remove('hidden');
        return;
      }
      
      studentId = data.student_id;
      studentName = name;
      quizType = data.quiz_type || 'option1';
      sessionCode = code;

      // Save session in localStorage
      localStorage.setItem('studentId', studentId);
      localStorage.setItem('sessionCode', sessionCode);
      localStorage.setItem('studentName', studentName);
      localStorage.setItem('quizType', quizType);

      initJoinedScreen();
    } catch (err) {
      errEl.textContent = 'Lỗi kết nối server.';
      errEl.classList.remove('hidden');
    } finally {
      btn.disabled = false;
      spinner.classList.add('hidden');
    }
  });
}

function initJoinedScreen() {
  document.getElementById('screenJoin').classList.add('hidden');
  if (quizType === 'option2') {
    document.getElementById('screenOption2').classList.remove('hidden');
    document.getElementById('studentNameO2').textContent = studentName;
    loadOption2State();
  } else {
    document.getElementById('screenOption1').classList.remove('hidden');
    document.getElementById('studentNameO1').textContent = studentName;
    initOption1();
  }
}

// ═══════════════════════════════════════════════════════
//  RETAKE QUIZ LOGIC
// ═══════════════════════════════════════════════════════
async function retakeQuiz() {
  const btn = document.getElementById('retakeBtn');
  btn.disabled = true;
  const originalText = btn.innerHTML;
  btn.textContent = 'Đang chuẩn bị...';

  try {
    const res = await fetch('/quiz/reset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: studentId })
    });
    const data = await res.json();
    if (!res.ok) {
      alert('Không thể làm lại bài thi: ' + (data.detail || 'Lỗi hệ thống'));
      btn.disabled = false;
      btn.innerHTML = originalText;
      return;
    }

    // Reset localStorage keys
    localStorage.removeItem('submitted_' + studentId);
    localStorage.removeItem('results_' + studentId);
    localStorage.removeItem('gridPlacement_' + studentId);
    localStorage.removeItem('completedSubQuizzes_' + studentId);
    localStorage.removeItem('subQuizScores_' + studentId);

    // Reset local state
    if (quizType === 'option1') {
      gridPlacement = Array.from({length: 7}, () => ({
        image_id: null,
        left_id: null,
        right_id: null,
        note_id: null,
        reason_id: null
      }));
      initOption1();
      document.getElementById('screenResult').classList.add('hidden');
      document.getElementById('screenOption1').classList.remove('hidden');
    } else {
      completedSubQuizzes = [];
      subQuizScores = {};
      updateOption2Dashboard();
      document.getElementById('screenResult').classList.add('hidden');
      document.getElementById('screenOption2').classList.remove('hidden');
    }

  } catch (err) {
    alert('Lỗi kết nối mạng: ' + err.message);
    btn.disabled = false;
    btn.innerHTML = originalText;
  }
}

// ═══════════════════════════════════════════════════════
//  AUTO-LOGIN & RESTORE SESSION ON LOAD
// ═══════════════════════════════════════════════════════
window.addEventListener('DOMContentLoaded', () => {
  const storedStudentId = localStorage.getItem('studentId');
  const storedSessionCode = localStorage.getItem('sessionCode');
  const storedStudentName = localStorage.getItem('studentName');
  
  if (storedStudentId && storedSessionCode && storedStudentName) {
    fetch('/quiz/active')
      .then(res => res.json())
      .then(data => {
        if (data.active && data.code === storedSessionCode) {
          studentId = parseInt(storedStudentId);
          studentName = storedStudentName;
          quizType = data.quiz_type || 'option1';
          sessionCode = storedSessionCode;
          
          const isSubmitted = localStorage.getItem('submitted_' + studentId);
          if (isSubmitted === 'true') {
            const savedResults = localStorage.getItem('results_' + studentId);
            if (savedResults) {
              try {
                const resultsObj = JSON.parse(savedResults);
                document.getElementById('screenJoin').classList.add('hidden');
                document.getElementById('screenResult').classList.remove('hidden');
                if (quizType === 'option1') {
                  const savedPlacement = localStorage.getItem('gridPlacement_' + studentId);
                  if (savedPlacement) gridPlacement = JSON.parse(savedPlacement);
                  showO1Results(resultsObj);
                } else {
                  const savedScores = localStorage.getItem('subQuizScores_' + studentId);
                  if (savedScores) subQuizScores = JSON.parse(savedScores);
                  showO2FinalResult(resultsObj.score, resultsObj.total);
                }
                return;
              } catch (e) {
                // ignore
              }
            }
          }
          
          restoreWipProgress();
          initJoinedScreen();
        } else {
          clearStudentSession();
        }
      })
      .catch(() => {
        // network error
      });
  }
});
