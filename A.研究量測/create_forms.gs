/**
 * RL Teaching — Google Forms Generator
 * 授課語言：英文（國際生）
 *
 * 使用方式：
 * 1. 前往 https://script.google.com → 新增專案
 * 2. 貼上此程式碼，取代原有內容
 * 3. 點選「執行」→ createAllForms()
 * 4. 第一次執行會跳授權視窗，允許即可
 * 5. 執行完畢後在「執行記錄」裡會印出兩個 Form 連結
 * 6. 開啟後測 Form，手動在 Section 2 的圖表判讀題插入對應圖片
 *
 * 產出：
 * - RL Teaching — Pre-Test（前測）
 * - RL Teaching — Post-Test（後測 + 問卷，含 3A/3B 分流）
 */

function createAllForms() {
  var preUrl  = createPreTest();
  var postUrl = createPostTest();
  Logger.log('=== Forms Created ===');
  Logger.log('Pre-Test  : ' + preUrl);
  Logger.log('Post-Test : ' + postUrl);
}

// ═══════════════════════════════════════════════════════
// PRE-TEST
// 結構：Section 0 基本資料 → Section 1 背景問卷 → Section 2 概念前測（15題）
// ═══════════════════════════════════════════════════════
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
    .setTitle('Q0-1  Student ID (anonymous code, e.g. CS1-23)')
    .setHelpText('Please use the same ID in the post-test so we can match your results.')
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Q0-2  Course / Class code')
    .setChoiceValues([
      'Programming (I) — Section A',
      'Programming (I) — Section B',
      'Other (please specify in Q0-1)'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Q0-3  Year of study')
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
    .setTitle('Q1-5  Confidence in math / probability (1 = not confident at all, 5 = very confident)')
    .setBounds(1, 5)
    .setLabels('Not confident at all', 'Very confident')
    .setRequired(true);

  form.addScaleItem()
    .setTitle('Q1-6  Interest in "AI that learns through trial and error" (1 = not interested, 5 = very interested)')
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

  var conceptQs = [
    // 2.1 基本概念
    {
      q: 'Q2-1  What is the core learning mechanism in reinforcement learning?',
      choices: [
        'A. A teacher provides the correct answer at every step',
        'B. The agent learns by trial and error, adjusting its strategy based on rewards and penalties',
        'C. The agent memorizes all possible states in advance',
        'D. A larger model always leads to better performance'
      ], ans: 'B'
    },
    {
      q: 'Q2-2  In reinforcement learning, which of the following best describes the "Agent"?',
      choices: [
        'A. The game map or environment layout',
        'B. The decision-maker that chooses actions',
        'C. The scoring system',
        'D. An obstacle in the environment'
      ], ans: 'B'
    },
    {
      q: 'Q2-3  Which of the following best describes the "Environment" in RL?',
      choices: [
        'A. The program responsible for selecting actions',
        'B. The world that provides observations, responds to actions, and returns results',
        'C. A function that only calculates the final score',
        'D. A database for storing training data'
      ], ans: 'B'
    },
    {
      q: 'Q2-4  What is the purpose of "Reward" in reinforcement learning?',
      choices: [
        'A. To serve as the input image for the agent',
        'B. To signal to the agent how good or bad its action was',
        'C. To replace the state information',
        'D. To guarantee the agent succeeds every time'
      ], ans: 'B'
    },
    {
      q: 'Q2-5  "State" in RL typically refers to?',
      choices: [
        'A. The current observation or situation (e.g. position, speed, remaining time)',
        'B. The action the agent will take next',
        'C. The score from the last episode',
        'D. The number of lines in the program'
      ], ans: 'A'
    },
    {
      q: 'Q2-6  "Action" in RL typically refers to?',
      choices: [
        'A. The current screen image',
        'B. The control command the agent can choose (e.g. left / right / jump)',
        'C. The reward value for each episode',
        'D. The number of training iterations'
      ], ans: 'B'
    },
    {
      q: 'Q2-7  An "Episode" in RL usually means?',
      choices: [
        'A. One page refresh',
        'B. One complete attempt from the initial state to a terminal state',
        'C. A single action selection',
        'D. One data download'
      ], ans: 'B'
    },
    // 2.2 探索與利用
    {
      q: 'Q2-8  Which of the following best describes "Exploration" in RL?',
      choices: [
        'A. Always choosing the action that currently looks best',
        'B. Trying different actions to gather more experience, even if short-term performance drops',
        'C. Taking no action at all',
        'D. Copying what other agents do'
      ], ans: 'B'
    },
    {
      q: 'Q2-9  Which of the following best describes "Exploitation" in RL?',
      choices: [
        'A. Selecting the action believed to be best based on accumulated experience',
        'B. Choosing randomly every time',
        'C. Never adjusting based on feedback',
        'D. Simply increasing training time'
      ], ans: 'A'
    },
    {
      q: 'Q2-10  If an agent "never explores" from the very beginning, what is most likely to happen?',
      choices: [
        'A. It will find the optimal strategy faster',
        'B. It may get stuck in a suboptimal strategy, having never tried better paths',
        'C. It becomes supervised learning',
        'D. The reward will automatically increase'
      ], ans: 'B'
    },
    // 2.3 長短期回報
    {
      q: 'Q2-11  Why does reinforcement learning often need to consider "long-term reward"?',
      choices: [
        'A. Because always maximizing the immediate reward will always lead to the best final outcome',
        'B. Some actions seem costly in the short term but lead to greater rewards in the future',
        'C. Because the environment is always random',
        'D. Because shorter code is always better'
      ], ans: 'B'
    },
    {
      q: 'Q2-12  If an agent strongly prioritizes "immediate reward", it might?',
      choices: [
        'A. Prefer short-term gains and miss better long-term outcomes',
        'B. Always find the shortest path through a maze',
        'C. Become completely random',
        'D. Lose access to state information'
      ], ans: 'A'
    },
    // 2.4 Q 值直覺
    {
      q: 'Q2-13  The intuition behind "Q-value" in Q-learning is most like?',
      choices: [
        'A. The expected total future reward of taking a specific action from a specific state',
        'B. The pixel values of the current screen',
        'C. The program execution time',
        'D. The player\'s input speed'
      ], ans: 'A'
    },
    {
      q: 'Q2-14  If Q(s, a) is large, it generally means?',
      choices: [
        'A. This action is always legally valid',
        'B. This choice is expected to lead to higher long-term reward',
        'C. This action always gives the shortest path',
        'D. The reward is always fixed'
      ], ans: 'B'
    },
    // 2.5 圖表判讀
    {
      q: 'Q2-15  During training, the average reward gradually increases and then levels off. The most reasonable explanation is?',
      choices: [
        'A. The agent is getting worse over time',
        'B. The agent has likely learned a better strategy and is converging',
        'C. The environment is broken',
        'D. This indicates no learning is happening'
      ], ans: 'B'
    }
  ];

  conceptQs.forEach(function(item) {
    form.addMultipleChoiceItem()
      .setTitle(item.q)
      .setChoiceValues(item.choices)
      .setRequired(true);
  });

  Logger.log('Pre-Test created: ' + form.getPublishedUrl());
  return form.getPublishedUrl();
}

// ═══════════════════════════════════════════════════════
// POST-TEST
// 結構：
//   Section 0  基本資料（含分組，用於後段分流）
//   Section 1  RL 概念後測（15 題，同前測，兩組共用）
//   Section 2  通用學習回饋量表（10 題 Likert，兩組共用）
//   Section 3A RR 平台體驗（只給實驗組）
//   Section 3B Colab 體驗（只給對照組）
//   Section 4  共同開放題（兩組共用）
// ═══════════════════════════════════════════════════════
function createPostTest() {
  var form = FormApp.create('RL Teaching — Post-Test & Feedback');
  form.setDescription(
    'Thank you for completing the class!\n' +
    'This form has 4 sections and takes about 25–30 minutes.\n' +
    'For Section 3, please fill in ONLY the section that matches your group (3A or 3B).\n' +
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

  form.addMultipleChoiceItem()
    .setTitle('Q0-2  Your group in this study')
    .setChoiceValues([
      'Group A — RR Platform (Rein Room)',
      'Group B — Gymnasium + Colab'
    ])
    .setRequired(true);

  // ── Section 1：RL 概念後測（15 題，同前測）─────────
  form.addPageBreakItem()
    .setTitle('Section 1 — RL Concept Test')
    .setHelpText(
      'Same questions as the pre-test. Answer based on what you know NOW. (15 questions)'
    );

  var postConceptQs = [
    {
      q: 'Q1-1  What is the core learning mechanism in reinforcement learning?',
      choices: [
        'A. A teacher provides the correct answer at every step',
        'B. The agent learns by trial and error, adjusting its strategy based on rewards and penalties',
        'C. The agent memorizes all possible states in advance',
        'D. A larger model always leads to better performance'
      ]
    },
    {
      q: 'Q1-2  In reinforcement learning, which best describes the "Agent"?',
      choices: [
        'A. The game map or environment layout',
        'B. The decision-maker that chooses actions',
        'C. The scoring system',
        'D. An obstacle in the environment'
      ]
    },
    {
      q: 'Q1-3  Which best describes the "Environment" in RL?',
      choices: [
        'A. The program responsible for selecting actions',
        'B. The world that provides observations, responds to actions, and returns results',
        'C. A function that only calculates the final score',
        'D. A database for storing training data'
      ]
    },
    {
      q: 'Q1-4  What is the purpose of "Reward" in reinforcement learning?',
      choices: [
        'A. To serve as the input image for the agent',
        'B. To signal to the agent how good or bad its action was',
        'C. To replace the state information',
        'D. To guarantee the agent succeeds every time'
      ]
    },
    {
      q: 'Q1-5  "State" in RL typically refers to?',
      choices: [
        'A. The current observation or situation (e.g. position, speed, remaining time)',
        'B. The action the agent will take next',
        'C. The score from the last episode',
        'D. The number of lines in the program'
      ]
    },
    {
      q: 'Q1-6  "Action" in RL typically refers to?',
      choices: [
        'A. The current screen image',
        'B. The control command the agent can choose (e.g. left / right / jump)',
        'C. The reward value for each episode',
        'D. The number of training iterations'
      ]
    },
    {
      q: 'Q1-7  An "Episode" in RL usually means?',
      choices: [
        'A. One page refresh',
        'B. One complete attempt from the initial state to a terminal state',
        'C. A single action selection',
        'D. One data download'
      ]
    },
    {
      q: 'Q1-8  Which best describes "Exploration" in RL?',
      choices: [
        'A. Always choosing the action that currently looks best',
        'B. Trying different actions to gather more experience, even if short-term performance drops',
        'C. Taking no action at all',
        'D. Copying what other agents do'
      ]
    },
    {
      q: 'Q1-9  Which best describes "Exploitation" in RL?',
      choices: [
        'A. Selecting the action believed to be best based on accumulated experience',
        'B. Choosing randomly every time',
        'C. Never adjusting based on feedback',
        'D. Simply increasing training time'
      ]
    },
    {
      q: 'Q1-10  If an agent "never explores" from the very beginning, what is most likely to happen?',
      choices: [
        'A. It will find the optimal strategy faster',
        'B. It may get stuck in a suboptimal strategy, having never tried better paths',
        'C. It becomes supervised learning',
        'D. The reward will automatically increase'
      ]
    },
    {
      q: 'Q1-11  Why does RL often need to consider "long-term reward"?',
      choices: [
        'A. Because always maximizing the immediate reward always leads to the best final outcome',
        'B. Some actions seem costly short-term but lead to greater rewards in the future',
        'C. Because the environment is always random',
        'D. Because shorter code is always better'
      ]
    },
    {
      q: 'Q1-12  If an agent strongly prioritizes "immediate reward", it might?',
      choices: [
        'A. Prefer short-term gains and miss better long-term outcomes',
        'B. Always find the shortest path through a maze',
        'C. Become completely random',
        'D. Lose access to state information'
      ]
    },
    {
      q: 'Q1-13  The intuition behind "Q-value" is most like?',
      choices: [
        'A. The expected total future reward of taking a specific action from a specific state',
        'B. The pixel values of the current screen',
        'C. The program execution time',
        'D. The player\'s input speed'
      ]
    },
    {
      q: 'Q1-14  If Q(s, a) is large, it generally means?',
      choices: [
        'A. This action is always legally valid',
        'B. This choice is expected to lead to higher long-term reward',
        'C. This action always gives the shortest path',
        'D. The reward is always fixed'
      ]
    },
    {
      q: 'Q1-15  During training, the average reward gradually increases and then levels off. The most reasonable explanation is?',
      choices: [
        'A. The agent is getting worse over time',
        'B. The agent has likely learned a better strategy and is converging',
        'C. The environment is broken',
        'D. This indicates no learning is happening'
      ]
    }
  ];

  postConceptQs.forEach(function(item) {
    form.addMultipleChoiceItem()
      .setTitle(item.q)
      .setChoiceValues(item.choices)
      .setRequired(true);
  });

  // ── Section 2：通用學習回饋量表（10 題，兩組共用）──
  form.addPageBreakItem()
    .setTitle('Section 2 — Learning Feedback (Both Groups)')
    .setHelpText('Rate each statement from 1 (Strongly Disagree) to 5 (Strongly Agree).');

  var sharedLikert = [
    'Q2-1  I now have a better understanding of what "State", "Action", and "Reward" each represent.',
    'Q2-2  I can explain the difference between "exploration" and "exploitation" in my own words.',
    'Q2-3  I can read a training result (e.g. reward trend over time) and explain what it means.',
    'Q2-4  This class helped me understand how AI learns through trial and error.',
    'Q2-5  I feel I could apply these concepts to other similar tasks (e.g. maze, control, decision problems).',
    'Q2-6  During the class, I actively tried different settings and tested my own ideas.',
    'Q2-7  I felt engaged and interested during the class.',
    'Q2-8  I felt frustrated during the class. (reverse-scored)',
    'Q2-9  The pace and difficulty level of the class felt appropriate.',
    'Q2-10  Overall, I am satisfied with this learning experience.'
  ];

  sharedLikert.forEach(function(title) {
    form.addScaleItem()
      .setTitle(title)
      .setBounds(1, 5)
      .setLabels('Strongly Disagree', 'Strongly Agree')
      .setRequired(true);
  });

  // ── Section 3A：RR 平台體驗（實驗組）────────────────
  form.addPageBreakItem()
    .setTitle('Section 3A — Platform Feedback   ★ Group A Only (Rein Room)')
    .setHelpText(
      'If you used the Rein Room (RR) platform, please fill in this section.\n' +
      'If you used Gymnasium + Colab, SKIP this section and scroll down to Section 3B.\n\n' +
      'Scale: 1 = Strongly Disagree → 5 = Strongly Agree'
    );

  var rrLikert = [
    'Q3A-1  I understood the operation flow of Rein Room (select task → start training → observe results).',
    'Q3A-2  Adjusting parameters with sliders made it easier for me to try different strategies.',
    'Q3A-3  The real-time visualizations (heatmap, reward curves) helped me understand what the agent was learning.',
    'Q3A-4  The workload of operating Rein Room was manageable.',
    'Q3A-5  I think Rein Room is a good tool for beginners to get started with RL.'
  ];

  rrLikert.forEach(function(title) {
    form.addScaleItem()
      .setTitle(title)
      .setBounds(1, 5)
      .setLabels('Strongly Disagree', 'Strongly Agree')
      .setRequired(false);
  });

  form.addParagraphTextItem()
    .setTitle('Q3A-6  What was the biggest difficulty you encountered while using Rein Room? (1–2 sentences, optional)')
    .setRequired(false);

  // ── Section 3B：Colab 體驗（對照組）─────────────────
  form.addPageBreakItem()
    .setTitle('Section 3B — Platform Feedback   ★ Group B Only (Gymnasium + Colab)')
    .setHelpText(
      'If you used Gymnasium + Colab, please fill in this section.\n' +
      'If you used Rein Room, SKIP this section and scroll down to Section 4.\n\n' +
      'Scale: 1 = Strongly Disagree → 5 = Strongly Agree'
    );

  var colabLikert = [
    'Q3B-1  I understood the training flow in Colab (e.g. reset / step concepts or the code structure).',
    'Q3B-2  Reading and modifying the code helped me understand how reinforcement learning works.',
    'Q3B-3  The operational workload in Colab (running cells, packages, plotting) was manageable.',
    'Q3B-4  I could understand the training process from the code output or charts.',
    'Q3B-5  I think Colab + Gymnasium is a good way for beginners to learn RL.'
  ];

  colabLikert.forEach(function(title) {
    form.addScaleItem()
      .setTitle(title)
      .setBounds(1, 5)
      .setLabels('Strongly Disagree', 'Strongly Agree')
      .setRequired(false);
  });

  form.addParagraphTextItem()
    .setTitle('Q3B-6  What was the biggest difficulty you encountered while using Colab + Gymnasium? (1–2 sentences, optional)')
    .setRequired(false);

  // ── Section 4：共同開放題（兩組共用）─────────────────
  form.addPageBreakItem()
    .setTitle('Section 4 — Open Feedback (Both Groups)');

  form.addParagraphTextItem()
    .setTitle('Q4-1  What was the most helpful part of this class for understanding reinforcement learning? Why?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Q4-2  What was the most confusing or difficult part of the class?')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Q4-3  If you could improve the platform or teaching materials, what would you change? (optional, 1–2 sentences)')
    .setRequired(false);

  Logger.log('Post-Test created: ' + form.getPublishedUrl());
  return form.getPublishedUrl();
}
