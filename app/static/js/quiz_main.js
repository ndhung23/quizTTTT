// ═══════════════════════════════════════════════════════
//  TAB SWITCH DETECTOR
// ═══════════════════════════════════════════════════════
let tabSwitchCount = 0;
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    tabSwitchCount++;
    console.log('Tab switched away! Count:', tabSwitchCount);
    if (studentId) {
      fetch('/quiz/tab-switch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: studentId, count: tabSwitchCount })
      }).catch(e => console.error(e));
    }
  }
});

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
      tabSwitchCount = data.tab_switch_count || 0;

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

async function loadQuizDefinitionAndStart() {
  try {
    const res = await fetch('/quiz/definition/' + quizType);
    if (!res.ok) {
      alert('Không thể tải cấu hình đề thi này từ server');
      return;
    }
    const data = await res.json();
    activeQuizSteps = data.steps || [];
    activeQuizTitle = data.title || 'Kiểm tra';
    const qFormat = data.quiz_format || 'option1';
    
    const titleHeader = document.getElementById('quizTitleHeader');
    if (titleHeader) titleHeader.textContent = activeQuizTitle;

    restoreWipProgress();

    document.getElementById('screenJoin').classList.add('hidden');
    document.getElementById('screenOption1').classList.add('hidden');
    document.getElementById('screenOption2').classList.add('hidden');
    document.getElementById('screenOption3').classList.add('hidden');
    document.getElementById('screenOption4').classList.add('hidden');
    document.getElementById('screenOption5').classList.add('hidden');

    if (qFormat === 'option3') {
      document.getElementById('screenOption3').classList.remove('hidden');
      document.getElementById('studentNameO3').textContent = studentName;
      initOption3();
    } else if (qFormat === 'option4') {
      document.getElementById('screenOption4').classList.remove('hidden');
      document.getElementById('studentNameO4').textContent = studentName;
      initOption4();
    } else if (qFormat === 'option5') {
      document.getElementById('screenOption5').classList.remove('hidden');
      document.getElementById('studentNameO5').textContent = studentName;
      document.getElementById('quizTitleHeaderO5').textContent = activeQuizTitle;
      initOption5();
    } else {
      document.getElementById('screenOption1').classList.remove('hidden');
      document.getElementById('studentNameO1').textContent = studentName;
      initOption1();
    }
  } catch (err) {
    alert('Lỗi kết nối khi tải đề thi: ' + err.message);
  }
}

function initJoinedScreen() {
  document.getElementById('screenJoin').classList.add('hidden');
  if (quizType === 'option2') {
    document.getElementById('screenOption2').classList.remove('hidden');
    document.getElementById('studentNameO2').textContent = studentName;
    loadOption2State();
  } else {
    loadQuizDefinitionAndStart();
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
    localStorage.removeItem('o3Answers_' + studentId);
    localStorage.removeItem('o4Answers_' + studentId);

    document.getElementById('screenResult').classList.add('hidden');

    // Reset local state & screens
    if (quizType !== 'option2') {
      const defRes = await fetch('/quiz/definition/' + quizType);
      if (defRes.ok) {
        const defData = await defRes.json();
        activeQuizSteps = defData.steps || [];
        activeQuizTitle = defData.title || 'Kiểm tra';
        const qFormat = defData.quiz_format || 'option1';

        document.getElementById('screenOption1').classList.add('hidden');
        document.getElementById('screenOption3').classList.add('hidden');
        document.getElementById('screenOption4').classList.add('hidden');
        document.getElementById('screenOption5').classList.add('hidden');

        if (qFormat === 'option3') {
          document.getElementById('screenOption3').classList.remove('hidden');
          initOption3();
        } else if (qFormat === 'option4') {
          document.getElementById('screenOption4').classList.remove('hidden');
          initOption4();
        } else if (qFormat === 'option5') {
          document.getElementById('screenOption5').classList.remove('hidden');
          document.getElementById('studentNameO5').textContent = studentName;
          document.getElementById('quizTitleHeaderO5').textContent = activeQuizTitle;
          initOption5();
        } else {
          gridPlacement = Array.from({length: activeQuizSteps.length}, () => ({
            image_id: null,
            left_id: null,
            right_id: null,
            note_id: null,
            reason_id: null
          }));
          currentPart = 1;
          document.getElementById('screenOption1').classList.remove('hidden');
          initOption1();
        }
      }
    } else {
      completedSubQuizzes = [];
      subQuizScores = {};
      updateOption2Dashboard();
      document.getElementById('screenOption2').classList.remove('hidden');
    }

  } catch (err) {
    alert('Lỗi kết nối mạng: ' + err.message);
  } finally {
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
      .then(async data => {
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
                if (quizType !== 'option2') {
                  // Fetch definition for rendering results
                  const defRes = await fetch('/quiz/definition/' + quizType);
                  if (defRes.ok) {
                    const defData = await defRes.json();
                    activeQuizSteps = defData.steps || [];
                    activeQuizTitle = defData.title || 'Kiểm tra';
                    const titleHeader = document.getElementById('quizTitleHeader');
                    if (titleHeader) titleHeader.textContent = activeQuizTitle;

                    const qFormat = defData.quiz_format || 'option1';
                    if (qFormat === 'option3') {
                      showO3Results(resultsObj);
                    } else if (qFormat === 'option4') {
                      showO4Results(resultsObj);
                    } else if (qFormat === 'option5') {
                      showOption5Result(resultsObj);
                    } else {
                      const savedPlacement = localStorage.getItem('gridPlacement_' + studentId);
                      if (savedPlacement) gridPlacement = JSON.parse(savedPlacement);
                      showO1Results(resultsObj);
                    }
                  }
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

          // Sync tab switch count from server
          fetch('/quiz/student-status/' + studentId)
            .then(res => res.json())
            .then(sData => {
              if (sData.ok) {
                tabSwitchCount = sData.tab_switch_count || 0;
              }
            }).catch(e => console.error(e));
        } else {
          clearStudentSession();
        }
      })
      .catch(() => {
        // network error
      });
  }

  // Restore saved theme on load
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'light') {
    document.body.classList.add('light-theme');
    const sunIcon = document.getElementById('themeSunIcon');
    const moonIcon = document.getElementById('themeMoonIcon');
    const toggleBtn = document.getElementById('themeToggleBtn');
    if (sunIcon) sunIcon.classList.remove('hidden');
    if (moonIcon) moonIcon.classList.add('hidden');
    if (toggleBtn) {
      toggleBtn.className = "fixed top-4 right-4 z-[99] bg-white hover:bg-slate-100 text-slate-800 p-2.5 rounded-xl border border-slate-200 shadow-lg transition duration-200 active:scale-95 flex items-center justify-center";
    }
  }
});

// ═══════════════════════════════════════════════════════
//  THEME TOGGLE LOGIC
// ═══════════════════════════════════════════════════════
function toggleTheme() {
  const body = document.body;
  const sunIcon = document.getElementById('themeSunIcon');
  const moonIcon = document.getElementById('themeMoonIcon');
  const toggleBtn = document.getElementById('themeToggleBtn');
  
  if (body.classList.contains('light-theme')) {
    body.classList.remove('light-theme');
    localStorage.setItem('theme', 'dark');
    if (sunIcon) sunIcon.classList.add('hidden');
    if (moonIcon) moonIcon.classList.remove('hidden');
    if (toggleBtn) {
      toggleBtn.className = "fixed top-4 right-4 z-[99] bg-slate-800 hover:bg-slate-700 text-yellow-400 p-2.5 rounded-xl border border-white/10 shadow-lg transition duration-200 active:scale-95 flex items-center justify-center";
    }
  } else {
    body.classList.add('light-theme');
    localStorage.setItem('theme', 'light');
    if (sunIcon) sunIcon.classList.remove('hidden');
    if (moonIcon) moonIcon.classList.add('hidden');
    if (toggleBtn) {
      toggleBtn.className = "fixed top-4 right-4 z-[99] bg-white hover:bg-slate-100 text-slate-800 p-2.5 rounded-xl border border-slate-200 shadow-lg transition duration-200 active:scale-95 flex items-center justify-center";
    }
  }
}
