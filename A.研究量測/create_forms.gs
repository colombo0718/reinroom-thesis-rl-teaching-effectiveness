/**
 * RL Teaching — Google Forms Generator
 * 授課語言：英文（國際生）
 *
 * 使用方式：
 * 1. 前往 https://script.google.com → 新增專案
 * 2. 貼上此程式碼，取代原有內容
 * 3. 點選「執行」→ createAllForms()
 * 4. 第一次執行會跳授權視窗，允許即可
 * 5. 執行完畢後在「執行記錄」裡會印出三個 Form 連結
 * 6. 在前測 Form Section 2 圖表題手動插入對應圖片
 *
 * 產出：
 * - RL Teaching — Pre-Test（前測，兩組共用）
 * - RL Teaching — Post-Test [Group A]（後測，實驗組）
 * - RL Teaching — Post-Test [Group B]（後測，對照組）
 *
 * 問卷結構：
 *   前測：Section 0 基本資料 → Section 1 背景問卷 → Section 2 概念前測（15題）
 *   後測：Section 0 基本資料 → Section 1 概念後測（15題）
 *         → Section 2 NASA-TLX（6題）→ Section 3 SUS（10題）
 *         → Section 4 平台回饋（5題 Likert）→ Section 5 開放題（3題）
 */

function createAllForms() {
  var preUrl   = createPreTest();
  var postAUrl = createPostTestA();  // Group A — Rein Room
  var postBUrl = createPostTestB();  // Group B — Gymnasium + Colab
  Logger.log('=== Forms Created ===');
  Logger.log('Pre-Test        : ' + preUrl);
  Logger.log('Post-Test [A]   : ' + postAUrl);
  Logger.log('Post-Test [B]   : ' + postBUrl);
}

// ═══════════════════════════════════════════════════════════════════
// 共用：前測 15 題概念題（pre-test 和 post-test 題目相同）
// ═══════════════════════════════════════════════════════════════════
var CONCEPT_QUESTIONS = [
  {
    q: 'What is the core learning mechanism in reinforcement learning?',
    choices: [
      'A. A teacher provides the correct answer at every step',
      'B. The agent learns by trial and error, adjusting its strategy based on rewards and penalties',
      'C. The agent memorizes all possible states in advance',
      'D. A larger model always leads to better performance'
    ]
  },
  {
    q: 'In reinforcement learning, which of the following best describes the "Agent"?',
    choices: [
      'A. The game map or environment layout',
      'B. The decision-maker that chooses actions',
      'C. The scoring system',
      'D. An obstacle in the environment'
    ]
  },
  {
    q: 'Which of the following best describes the "Environment" in RL?',
    choices: [
      'A. The program responsible for selecting actions',
      'B. The world that provides observations, responds to actions, and returns results',
      'C. A function that only calculates the final score',
      'D. A database for storing training data'
    ]
  },
  {
    q: 'What is the purpose of "Reward" in reinforcement learning?',
    choices: [
      'A. To serve as the input image for the agent',
      'B. To signal to the agent how good or bad its action was',
      'C. To replace the state information',
      'D. To guarantee the agent succeeds every time'
    ]
  },
  {
    q: '"State" in RL typically refers to?',
    choices: [
      'A. The current observation or situation (e.g. position, speed, remaining time)',
      'B. The action the agent will take next',
      'C. The score from the last episode',
      'D. The number of lines in the program'
    ]
  },
  {
    q: '"Action" in RL typically refers to?',
    choices: [
      'A. The current screen image',
      'B. The control command the agent can choose (e.g. left / right / jump)',
      'C. The reward value for each episode',
      'D. The number of training iterations'
    ]
  },
  {
    q: 'An "Episode" in RL usually means?',
    choices: [
      'A. One page refresh',
      'B. One complete attempt from the initial state to a terminal state',
      'C. A single action selection',
      'D. One data download'
    ]
  },
  {
    q: 'Which of the following best describes "Exploration" in RL?',
    choices: [
      'A. Always choosing the action that currently looks best',
      'B. Trying different actions to gather more experience, even if short-term performance drops',
      'C. Taking no action at all',
      'D. Copying what other agents do'
    ]
  },
  {
    q: 'Which of the following best describes "Exploitation" in RL?',
    choices: [
      'A. Selecting the action believed to be best based on accumulated experience',
      'B. Choosing randomly every time',
      'C. Never adjusting based on feedback',
      'D. Simply increasing training time'
    ]
  },
  {
    q: 'If an agent "never explores" from the very beginning, what is most likely to happen?',
    choices: [
      'A. It will find the optimal strategy faster',
      'B. It may get stuck in a suboptimal strategy, having never tried better paths',
      'C. It becomes supervised learning',
      'D. The reward will automatically increase'
    ]
  },
  {
    q: 'Why does reinforcement learning often need to consider "long-term reward"?',
    choices: [
      'A. Because always maximizing the immediate reward will always lead to the best final outcome',
      'B. Some actions seem costly in the short term but lead to greater rewards in the future',
      'C. Because the environment is always random',
      'D. Because shorter code is always better'
    ]
  },
  {
    q: 'If an agent strongly prioritizes "immediate reward", it might?',
    choices: [
      'A. Prefer short-term gains and miss better long-term outcomes',
      'B. Always find the shortest path through a maze',
      'C. Become completely random',
      'D. Lose access to state information'
    ]
  },
  {
    q: 'The intuition behind "Q-value" in Q-learning is most like?',
    choices: [
      'A. The expected total future reward of taking a specific action from a specific state',
      'B. The pixel values of the current screen',
      'C. The program execution time',
      'D. The player\'s input speed'
    ]
  },
  {
    q: 'If Q(s, a) is large, it generally means?',
    choices: [
      'A. This action is always legally valid',
      'B. This choice is expected to lead to higher long-term reward',
      'C. This action always gives the shortest path',
      'D. The reward is always fixed'
    ]
  },
  {
    q: 'During training, the average reward gradually increases and then levels off. The most reasonable explanation is?',
    choices: [
      'A. The agent is getting worse over time',
      'B. The agent has likely learned a better strategy and is converging',
      'C. The environment is broken',
      'D. This indicates no learning is happening'
    ]
  }
];

// ── NASA-TLX 題目（6題，1-10分）────────────────────────────────────
// 量表說明：1 = Very Low（非常低）, 10 = Very High（非常高）
// Performance 方向相反：1 = Perfect, 10 = Failure（填寫時需注意，分析時反向計分）
var NASA_TLX = [
  {
    title: 'NASA-1  Mental Demand',
    help:  'How much mental and perceptual activity was required? (e.g. thinking, deciding, calculating, remembering, looking, searching)\n1 = Very Low  →  10 = Very High'
  },
  {
    title: 'NASA-2  Temporal Demand',
    help:  'How much time pressure did you feel during the task? Were things rushed or slow and leisurely?\n1 = Very Low  →  10 = Very High'
  },
  {
    title: 'NASA-3  Performance',
    help:  'How successful do you think you were in accomplishing the goals of the task?\n1 = Perfect  →  10 = Failure  (reverse-scored)'
  },
  {
    title: 'NASA-4  Effort',
    help:  'How hard did you have to work (mentally and physically) to accomplish your level of performance?\n1 = Very Low  →  10 = Very High'
  },
  {
    title: 'NASA-5  Frustration',
    help:  'How insecure, discouraged, irritated, stressed, and annoyed were you during the task?\n1 = Very Low  →  10 = Very High'
  },
  {
    title: 'NASA-6  Overall Workload',
    help:  'Considering all the above dimensions together, how would you rate the overall workload of using the system today?\n1 = Very Low  →  10 = Very High'
  }
];

// ── SUS 系統易用性量表（10題，1-5分）──────────────────────────────
// 標準 SUS，奇數題正向、偶數題負向（計分時 ±4 然後 ×2.5 = 0-100）
// systemName 傳入後替換 "this system"
function getSusItems(systemName) {
  return [
    'SUS-1   I think that I would like to use ' + systemName + ' frequently.',
    'SUS-2   I found ' + systemName + ' unnecessarily complex.',
    'SUS-3   I thought ' + systemName + ' was easy to use.',
    'SUS-4   I think that I would need the support of a technical person to be able to use ' + systemName + '.',
    'SUS-5   I found the various functions in ' + systemName + ' were well integrated.',
    'SUS-6   I thought there was too much inconsistency in ' + systemName + '.',
    'SUS-7   I would imagine that most people would learn to use ' + systemName + ' very quickly.',
    'SUS-8   I found ' + systemName + ' very cumbersome to use.',
    'SUS-9   I felt very confident using ' + systemName + '.',
    'SUS-10  I needed to learn a lot of things before I could get going with ' + systemName + '.'
  ];
}

// ── 共用函式：加入概念題 ────────────────────────────────────────────
function addConceptQuestions(form, prefix) {
  CONCEPT_QUESTIONS.forEach(function(item, i) {
    form.addMultipleChoiceItem()
      .setTitle(prefix + (i + 1) + '  ' + item.q)
      .setChoiceValues(item.choices)
      .setRequired(true);
  });
}

// ── 共用函式：加入 NASA-TLX ─────────────────────────────────────────
function addNasaTlx(form) {
  form.addPageBreakItem()
    .setTitle('Section 2 — NASA-TLX  (Workload Assessment)')
    .setHelpText(
      'These 6 questions assess how demanding the learning activity felt today.\n' +
      'Rate each dimension from 1 to 10.'
    );
  NASA_TLX.forEach(function(item) {
    form.addScaleItem()
      .setTitle(item.title)
      .setHelpText(item.help)
      .setBounds(1, 10)
      .setLabels('Very Low / Perfect', 'Very High / Failure')
      .setRequired(true);
  });
}

// ── 共用函式：加入 SUS ──────────────────────────────────────────────
function addSus(form, systemName) {
  form.addPageBreakItem()
    .setTitle('Section 3 — SUS  (System Usability Scale)')
    .setHelpText(
      'Rate each statement from 1 (Strongly Disagree) to 5 (Strongly Agree).\n' +
      '"' + systemName + '" refers to the platform / tool you used today.'
    );
  getSusItems(systemName).forEach(function(title) {
    form.addScaleItem()
      .setTitle(title)
      .setBounds(1, 5)
      .setLabels('Strongly Disagree', 'Strongly Agree')
      .setRequired(true);
  });
}

// ── 共用函式：加入開放題 ────────────────────────────────────────────
function addOpenQuestions(form) {
  form.addPageBreakItem()
    .setTitle('Section 5 — Open Feedback');

  form.addParagraphTextItem()
    .setTitle('Q5-1  What was the most helpful part of this class for understanding reinforcement learning? Why?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Q5-2  What was the most confusing or difficult part of the class?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Q5-3  If you could improve the platform or teaching materials, what would you change? (optional)')
    .setRequired(false);
}


// ═══════════════════════════════════════════════════════════════════
// PRE-TEST（前測，兩組共用）
// ═══════════════════════════════════════════════════════════════════
function createPreTest() {
  var form = FormApp.create('RL Teaching — Pre-Test');
  form.setDescription(
    'This questionnaire is for research purposes only. ' +
    'Your answers are anonymous and will NOT affect your grade.\n' +
    'Please answer honestly — it is completely fine if you have no prior knowledge of RL.\n' +
    'Estimated time: 15–20 minutes.'
  );
  form.setIsQuiz(false);
  form.setCollectEmail(false);

  // ── Section 0：基本資料 ────────────────────────────
  form.addSectionHeaderItem()
    .setTitle('Section 0 — Basic Information');

  form.addTextItem()
    .setTitle('Q0-1  Student ID (anonymous code, e.g. A-23)')
    .setHelpText('Please use the same ID in the post-test so we can match your results.')
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Q0-2  Year of study')
    .setChoiceValues(['1st year', '2nd year', '3rd year', '4th year', "Graduate (Master's)"])
    .setRequired(true);

  // ── Section 1：背景問卷（6 題）────────────────────
  form.addPageBreakItem()
    .setTitle('Section 1 — Background Survey');

  form.addMultipleChoiceItem()
    .setTitle('Q1-1  Programming experience')
    .setChoiceValues([
      'A. Almost none (< 1 month)',
      'B. Beginner (1–6 months)',
      'C. Intermediate (6–12 months)',
      'D. Experienced (> 1 year)'
    ])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('Q1-2  Programming language(s) you have used (select all that apply)')
    .setChoiceValues(['Python', 'Java', 'JavaScript', 'C / C++', 'Other'])
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('Q1-3  Have you written code that makes autonomous decisions or choices?')
    .setChoiceValues([
      'A. No',
      'B. Yes — simple if/else rules',
      'C. Yes — search or optimization (e.g. BFS, shortest path)',
      'D. Yes — machine learning (classification, regression, etc.)'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Q1-4  Prior exposure to AI / machine learning / reinforcement learning')
    .setChoiceValues([
      'A. None at all',
      'B. Heard of it but do not understand it',
      'C. Took a related course or worked on a related project'
    ])
    .setRequired(true);

  form.addScaleItem()
    .setTitle('Q1-5  Confidence in math / probability')
    .setBounds(1, 5)
    .setLabels('Not confident at all', 'Very confident')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('Q1-6  Interest in "AI that learns through trial and error"')
    .setBounds(1, 5)
    .setLabels('Not interested', 'Very interested')
    .setRequired(true);

  // ── Section 2：RL 概念前測（15 題）────────────────
  form.addPageBreakItem()
    .setTitle('Section 2 — RL Concept Test')
    .setHelpText(
      '15 single-choice questions. Choose the best answer.\n' +
      'There is no penalty for wrong answers — please give your best guess.'
    );

  addConceptQuestions(form, 'Q2-');

  Logger.log('Pre-Test created: ' + form.getPublishedUrl());
  return form.getPublishedUrl();
}


// ═══════════════════════════════════════════════════════════════════
// POST-TEST — GROUP A（實驗組，Rein Room 平台）
// ═══════════════════════════════════════════════════════════════════
function createPostTestA() {
  var form = FormApp.create('RL Teaching — Post-Test [Group A]');
  form.setDescription(
    'Thank you for completing the class!\n' +
    'This form has 5 sections and takes about 25–30 minutes.\n' +
    'Your answers are anonymous and will NOT affect your grade.'
  );
  form.setIsQuiz(false);
  form.setCollectEmail(false);

  // ── Section 0：基本資料 ────────────────────────────
  form.addSectionHeaderItem()
    .setTitle('Section 0 — Basic Information');

  form.addTextItem()
    .setTitle('Q0-1  Student ID (same as your pre-test ID)')
    .setRequired(true);

  // ── Section 1：RL 概念後測（15 題，同前測）─────────
  form.addPageBreakItem()
    .setTitle('Section 1 — RL Concept Test')
    .setHelpText('Same questions as the pre-test. Answer based on what you know NOW. (15 questions)');

  addConceptQuestions(form, 'Q1-');

  // ── Section 2：NASA-TLX ──────────────────────────
  addNasaTlx(form);

  // ── Section 3：SUS（Rein Room）───────────────────
  addSus(form, 'Rein Room');

  // ── Section 4：平台回饋量表（Rein Room 專屬）──────
  form.addPageBreakItem()
    .setTitle('Section 4 — Platform Feedback')
    .setHelpText('Rate each statement from 1 (Strongly Disagree) to 5 (Strongly Agree).');

  var rrFeedback = [
    'Q4-1  I understood the overall operation flow of the platform (select task → adjust parameters → start training → observe results).',
    'Q4-2  Adjusting parameters with sliders made it easier to try different strategies.',
    'Q4-3  The real-time visualizations (reward curve, Q-table heatmap) helped me understand what the agent was learning.',
    'Q4-4  The workload of operating the platform during class was manageable.',
    'Q4-5  I am more interested in learning about reinforcement learning after today\'s class.'
  ];

  rrFeedback.forEach(function(title) {
    form.addScaleItem()
      .setTitle(title)
      .setBounds(1, 5)
      .setLabels('Strongly Disagree', 'Strongly Agree')
      .setRequired(true);
  });

  // ── Section 5：開放題 ─────────────────────────────
  addOpenQuestions(form);

  Logger.log('Post-Test [Group A] created: ' + form.getPublishedUrl());
  return form.getPublishedUrl();
}


// ═══════════════════════════════════════════════════════════════════
// POST-TEST — GROUP B（對照組，Gymnasium + Colab）
// ═══════════════════════════════════════════════════════════════════
function createPostTestB() {
  var form = FormApp.create('RL Teaching — Post-Test [Group B]');
  form.setDescription(
    'Thank you for completing the class!\n' +
    'This form has 5 sections and takes about 25–30 minutes.\n' +
    'Your answers are anonymous and will NOT affect your grade.'
  );
  form.setIsQuiz(false);
  form.setCollectEmail(false);

  // ── Section 0：基本資料 ────────────────────────────
  form.addSectionHeaderItem()
    .setTitle('Section 0 — Basic Information');

  form.addTextItem()
    .setTitle('Q0-1  Student ID (same as your pre-test ID)')
    .setRequired(true);

  // ── Section 1：RL 概念後測（15 題，同前測）─────────
  form.addPageBreakItem()
    .setTitle('Section 1 — RL Concept Test')
    .setHelpText('Same questions as the pre-test. Answer based on what you know NOW. (15 questions)');

  addConceptQuestions(form, 'Q1-');

  // ── Section 2：NASA-TLX ──────────────────────────
  addNasaTlx(form);

  // ── Section 3：SUS（Colab + Gymnasium）───────────
  addSus(form, 'Colab + Gymnasium');

  // ── Section 4：平台回饋量表（Colab 專屬）──────────
  form.addPageBreakItem()
    .setTitle('Section 4 — Platform Feedback')
    .setHelpText('Rate each statement from 1 (Strongly Disagree) to 5 (Strongly Agree).');

  var colabFeedback = [
    'Q4-1  I understood the overall training flow in the notebook (e.g. the code structure, what each cell does).',
    'Q4-2  Reading and modifying the parameters in the code helped me understand how reinforcement learning works.',
    'Q4-3  The charts generated by the code helped me understand what the agent was learning.',
    'Q4-4  The workload of running the notebook during class was manageable.',
    'Q4-5  I am more interested in learning about reinforcement learning after today\'s class.'
  ];

  colabFeedback.forEach(function(title) {
    form.addScaleItem()
      .setTitle(title)
      .setBounds(1, 5)
      .setLabels('Strongly Disagree', 'Strongly Agree')
      .setRequired(true);
  });

  // ── Section 5：開放題 ─────────────────────────────
  addOpenQuestions(form);

  Logger.log('Post-Test [Group B] created: ' + form.getPublishedUrl());
  return form.getPublishedUrl();
}
