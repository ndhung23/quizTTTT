// ═══════════════════════════════════════════════════════
//  APP STATE
// ═══════════════════════════════════════════════════════
let studentId = null;
let studentName = '';
let quizType = 'option1';
let sessionCode = '';

// Option 1 Grid State
// gridPlacement[row_idx][col_name] = id (1..23)
let gridPlacement = Array.from({length: 23}, () => ({
  image_id: null,
  left_id: null,
  right_id: null,
  note_id: null,
  reason_id: null
}));

let currentPart = 1; // 1: Steps 1-7, 2: Steps 8-15, 3: Steps 16-23

// Option 2 State
let completedSubQuizzes = [];
let subQuizScores = {};
let activeSubQuizId = null;

// Selected puzzle item from the pool for Option 1 click-to-place
let selectedPoolItem = null;

// ═══════════════════════════════════════════════════════
//  STATE UTILS
// ═══════════════════════════════════════════════════════
function shuffle(array) {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

function clearStudentSession() {
  localStorage.removeItem('studentId');
  localStorage.removeItem('sessionCode');
  localStorage.removeItem('studentName');
  localStorage.removeItem('quizType');
  for (let i = localStorage.length - 1; i >= 0; i--) {
    const key = localStorage.key(i);
    if (key && (key.startsWith('gridPlacement_') || 
                key.startsWith('completedSubQuizzes_') || 
                key.startsWith('subQuizScores_') || 
                key.startsWith('submitted_') || 
                key.startsWith('results_'))) {
      localStorage.removeItem(key);
    }
  }
}

function restoreWipProgress() {
  const savedPlacement = localStorage.getItem('gridPlacement_' + studentId);
  if (savedPlacement) {
    try {
      gridPlacement = JSON.parse(savedPlacement);
    } catch (e) {
      // ignore
    }
  }

  const savedCompleted = localStorage.getItem('completedSubQuizzes_' + studentId);
  const savedScores = localStorage.getItem('subQuizScores_' + studentId);
  if (savedCompleted && savedScores) {
    try {
      completedSubQuizzes = JSON.parse(savedCompleted);
      subQuizScores = JSON.parse(savedScores);
    } catch (e) {
      // ignore
    }
  }
}
