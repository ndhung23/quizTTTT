// ═══════════════════════════════════════════════════════
//  APP STATE
// ═══════════════════════════════════════════════════════
let studentId = null;
let studentName = '';
let quizType = 'option1';
let sessionCode = '';

let activeQuizSteps = [];
let activeQuizTitle = '';

// Option 1 Grid State
// gridPlacement[row_idx][col_name] = id (1..N)
let gridPlacement = [];

let currentPart = 1; // 1: Part 1, 2: Part 2, etc.

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
                key.startsWith('o3Answers_') || 
                key.startsWith('o4Answers_') || 
                key.startsWith('submitted_') || 
                key.startsWith('results_'))) {
      localStorage.removeItem(key);
    }
  }
}

function restoreWipProgress() {
  // Initialize gridPlacement with correct length
  const expectedLen = activeQuizSteps.length || 23;
  gridPlacement = Array.from({length: expectedLen}, () => ({
    image_id: null,
    left_id: null,
    right_id: null,
    note_id: null,
    reason_id: null
  }));

  const savedPlacement = localStorage.getItem('gridPlacement_' + studentId);
  if (savedPlacement) {
    try {
      const parsed = JSON.parse(savedPlacement);
      if (Array.isArray(parsed) && parsed.length === expectedLen) {
        gridPlacement = parsed;
      }
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
