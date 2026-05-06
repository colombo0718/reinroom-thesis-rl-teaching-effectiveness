/**
 * RL Lab — All Forms Generator (with auto chart insertion)
 *
 * 使用方式：
 *   1. 開啟 script.google.com → New project
 *   2. 貼上全部程式碼，存檔
 *   3. 選擇函式 createAllForms，點執行
 *   4. 授權後，執行記錄會印出 4 個表單的連結
 *
 * ✅ Section 2 的三張圖表會自動插入，不需手動操作
 */

// ═══════════════════════════════════════════════════════════
// CHART IMAGE URLs (from public GitHub repo)
// ═══════════════════════════════════════════════════════════

var CHART_BASE = 'https://raw.githubusercontent.com/colombo0718/rl-lab-group-b/master/';

var CHARTS = {
  q2_1: CHART_BASE + 'chart_q2_1.png',
  q2_2: CHART_BASE + 'chart_q2_2.png',
  q2_3: CHART_BASE + 'chart_q2_3.png',
};

// ═══════════════════════════════════════════════════════════
// ENTRY POINT — 執行這個
// ═══════════════════════════════════════════════════════════

function createAllForms() {
  Logger.log('Fetching chart images...');
  var chartBlobs = {
    q2_1: UrlFetchApp.fetch(CHARTS.q2_1).getBlob().setName('chart_q2_1.png'),
    q2_2: UrlFetchApp.fetch(CHARTS.q2_2).getBlob().setName('chart_q2_2.png'),
    q2_3: UrlFetchApp.fetch(CHARTS.q2_3).getBlob().setName('chart_q2_3.png'),
  };
  Logger.log('Charts fetched. Building forms...');

  var results = [];
  results.push({ label: 'Pre-test  A', form: _buildPreTest('A', chartBlobs)  });
  results.push({ label: 'Pre-test  B', form: _buildPreTest('B', chartBlobs)  });
  results.push({ label: 'Post-test A', form: _buildPostTest('A', chartBlobs) });
  results.push({ label: 'Post-test B', form: _buildPostTest('B', chartBlobs) });

  Logger.log('\n✅  All 4 forms created!\n');
  results.forEach(function(r) {
    Logger.log('── ' + r.label + ' ──────────────────────────');
    Logger.log('   Edit : ' + r.form.getEditUrl());
    Logger.log('   Share: ' + r.form.getPublishedUrl());
  });
}

// ═══════════════════════════════════════════════════════════
// PRE-TEST BUILDER
// ═══════════════════════════════════════════════════════════

function _buildPreTest(group, blobs) {
  var form = FormApp.create('RL Lab — Pre-Test (Group ' + group + ')');
  form.setDescription(
    'This form is for research data collection only and does NOT affect your course grade.\n' +
    'Estimated time: ~15 minutes.\n\n' +
    'Please create a short Student ID you can remember — you will use the same ID in the post-test.'
  );
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage('Thank you! Your pre-test response has been recorded.');

  // ── Section 0: Basic Information ─────────────────────────
  form.addTextItem()
    .setTitle('Student ID')
    .setHelpText('Create a short anonymous code (e.g., your initials + last 2 digits of student number).')
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Year of study')
    .setChoiceValues(['1st year', '2nd year', '3rd year', '4th year', 'Graduate or above'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Programming experience')
    .setChoiceValues(['None', 'Basic (< 6 months)', 'Intermediate (6–12 months)', 'Advanced (> 1 year)'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Prior knowledge of reinforcement learning')
    .setChoiceValues(['Never heard of it', 'Heard of it but don\'t understand', 'Some understanding', 'Familiar with it'])
    .setRequired(true);

  _addRLConceptSection(form);
  _addChartSection(form, blobs);

  return form;
}

// ═══════════════════════════════════════════════════════════
// POST-TEST BUILDER
// ═══════════════════════════════════════════════════════════

function _buildPostTest(group, blobs) {
  var isA = (group === 'A');
  var platformName = isA ? 'Rein Room' : 'Google Colab';

  var form = FormApp.create('RL Lab — Post-Test (Group ' + group + ')');
  form.setDescription(
    'This form is for research data collection only and does NOT affect your course grade.\n' +
    'Estimated time: ~25 minutes.\n\n' +
    'Please enter the same Student ID you used in the pre-test.'
  );
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage('Thank you! Your post-test response has been recorded.');

  // ── Section 0: Basic Information ─────────────────────────
  form.addTextItem()
    .setTitle('Student ID')
    .setHelpText('Enter the same anonymous code you used in the pre-test.')
    .setRequired(true);

  _addRLConceptSection(form);
  _addChartSection(form, blobs);

  // ── Section 3: Platform Feedback ─────────────────────────
  form.addPageBreakItem()
    .setTitle('Section 3: Platform Experience — ' + platformName)
    .setHelpText('Rate each statement from 1 (Strongly Disagree) to 5 (Strongly Agree).');

  if (isA) {
    _likert5(form, '3-1.  The Rein Room interface was easy to use.');
    _likert5(form, '3-2.  I felt confident adjusting the parameters (α, γ, ε) using the sliders.');
    _likert5(form, '3-3.  The visualizations (heatmap, reward curves) helped me understand what the agent was learning.');
    _likert5(form, '3-4.  I am interested in learning more about reinforcement learning after this class.');
    _likert5(form, '3-5.  I would recommend Rein Room to someone who wants to learn about RL.');
  } else {
    _likert5(form, '3-1.  The Colab interface was easy to use.');
    _likert5(form, '3-2.  I felt confident modifying the parameters (alpha, gamma, epsilon) in the code.');
    _likert5(form, '3-3.  The charts generated by the code helped me understand what the agent was learning.');
    _likert5(form, '3-4.  I am interested in learning more about reinforcement learning after this class.');
    _likert5(form, '3-5.  I would recommend Colab + the course notebooks to someone who wants to learn about RL.');
  }

  // ── Section 4: NASA-TLX ───────────────────────────────────
  form.addPageBreakItem()
    .setTitle('Section 4: Task Load Index (NASA-TLX)')
    .setHelpText('Rate each dimension based on your experience during today\'s activities.  1 = Very Low · 10 = Very High');

  _scale10(form, '4-1.  Mental Demand — How much mental and perceptual activity was required?');
  _scale10(form, '4-2.  Physical Demand — How much physical activity was required? (clicking, scrolling, typing, etc.)');
  _scale10(form, '4-3.  Temporal Demand — How much time pressure did you feel during the tasks?');
  form.addScaleItem()
    .setTitle('4-4.  Performance — How successful do you think you were in accomplishing the goals?')
    .setBounds(1, 10).setLabels('Perfect', 'Failure').setRequired(true);
  _scale10(form, '4-5.  Effort — How hard did you have to work to accomplish your level of performance?');
  _scale10(form, '4-6.  Frustration — How insecure, discouraged, irritated, stressed, or annoyed did you feel?');

  // ── Section 5: SUS ────────────────────────────────────────
  form.addPageBreakItem()
    .setTitle('Section 5: System Usability Scale (SUS) — ' + platformName)
    .setHelpText('Rate each statement from 1 (Strongly Disagree) to 5 (Strongly Agree).');

  if (isA) {
    _likert5(form, '5-1.  I think that I would like to use Rein Room frequently.');
    _likert5(form, '5-2.  I found Rein Room unnecessarily complex.');
    _likert5(form, '5-3.  I thought Rein Room was easy to use.');
    _likert5(form, '5-4.  I think that I would need the support of a technical person to be able to use Rein Room.');
    _likert5(form, '5-5.  I found the various functions in Rein Room were well integrated.');
    _likert5(form, '5-6.  I thought there was too much inconsistency in Rein Room.');
    _likert5(form, '5-7.  I would imagine that most people would learn to use Rein Room very quickly.');
    _likert5(form, '5-8.  I found Rein Room very cumbersome to use.');
    _likert5(form, '5-9.  I felt very confident using Rein Room.');
    _likert5(form, '5-10.  I needed to learn a lot of things before I could get going with Rein Room.');
  } else {
    _likert5(form, '5-1.  I think that I would like to use Google Colab with these notebooks frequently.');
    _likert5(form, '5-2.  I found the Colab + notebook setup unnecessarily complex.');
    _likert5(form, '5-3.  I thought the Colab + notebook setup was easy to use.');
    _likert5(form, '5-4.  I think that I would need the support of a technical person to be able to use the Colab notebooks.');
    _likert5(form, '5-5.  I found the various parts of the Colab notebooks were well integrated.');
    _likert5(form, '5-6.  I thought there was too much inconsistency in how the Colab notebooks worked.');
    _likert5(form, '5-7.  I would imagine that most people would learn to use these Colab notebooks very quickly.');
    _likert5(form, '5-8.  I found the Colab + notebook setup very cumbersome to use.');
    _likert5(form, '5-9.  I felt very confident using Google Colab for this course.');
    _likert5(form, '5-10.  I needed to learn a lot of things before I could get going with the Colab notebooks.');
  }

  // ── Section 6: Open Feedback ──────────────────────────────
  form.addPageBreakItem()
    .setTitle('Section 6: Overall Feedback')
    .setHelpText('Short answers welcome (1–3 sentences each).');

  form.addParagraphTextItem()
    .setTitle('6-1.  What was the most helpful part of today\'s class?')
    .setRequired(true);
  form.addParagraphTextItem()
    .setTitle('6-2.  What was the most confusing or difficult part?')
    .setRequired(true);
  form.addParagraphTextItem()
    .setTitle('6-3.  Any other comments or suggestions? (optional)')
    .setRequired(false);

  return form;
}

// ═══════════════════════════════════════════════════════════
// SHARED SECTION BUILDERS
// ═══════════════════════════════════════════════════════════

function _addRLConceptSection(form) {
  form.addPageBreakItem()
    .setTitle('Section 1: RL Concept Questions')
    .setHelpText('Choose the best answer for each question.  (5 questions · 1 pt each)');

  _mc(form, '1-1.  In reinforcement learning, what does "state" refer to?',
    ['A.  The action taken by the agent',
     'B.  The current observation of the environment',
     'C.  The reward received',
     'D.  The learning rate'], 1);

  _mc(form, '1-2.  What happens at the start of a new "episode"?',
    ['A.  The agent receives a large reward',
     'B.  The Q-table is cleared',
     'C.  The environment resets to the initial condition',
     'D.  The agent stops exploring'], 2);

  _mc(form, '1-3.  In an ε-greedy strategy, what does a HIGH ε value mean?',
    ['A.  The agent always picks the best known action',
     'B.  The agent explores more randomly',
     'C.  The agent learns faster',
     'D.  The agent ignores all rewards'], 1);

  _mc(form, '1-4.  Which of the following best describes what Q(s, a) represents?',
    ['A.  The probability of choosing action a from state s',
     'B.  The immediate reward for taking action a',
     'C.  The expected future reward when taking action a from state s',
     'D.  The number of times action a was taken'], 2);

  _mc(form, '1-5.  If an agent always picks the action with the highest Q-value and never tries anything new, what problem might occur?',
    ['A.  The agent learns too slowly',
     'B.  The agent might miss a better action it has never tried',
     'C.  The Q-table grows too large',
     'D.  The reward curve becomes too smooth'], 1);
}

function _addChartSection(form, blobs) {
  form.addPageBreakItem()
    .setTitle('Section 2: Chart Interpretation')
    .setHelpText('Look at each chart carefully before answering.  (3 questions · 1 pt each)');

  // Q2-1
  form.addImageItem().setImage(blobs.q2_1).setWidth(560);
  _mc(form, '2-1.  A reward curve stays flat for the first 100 episodes, then steadily increases. What does this most likely indicate?',
    ['A.  The agent stopped exploring after episode 100',
     'B.  The agent began learning effectively around episode 100',
     'C.  The reward function changed at episode 100',
     'D.  The agent reached the maximum possible reward'], 1);

  // Q2-2
  form.addImageItem().setImage(blobs.q2_2).setWidth(560);
  _mc(form, '2-2.  Two reward curves are shown: Curve A rises quickly but is noisy and unstable. Curve B rises slowly but is smooth and steady. Which statement is most likely correct?',
    ['A.  Curve A has a lower learning rate than Curve B',
     'B.  Curve A has a higher learning rate than Curve B',
     'C.  Curve B has a higher exploration rate than Curve A',
     'D.  Both curves used the same parameters'], 1);

  // Q2-3
  form.addImageItem().setImage(blobs.q2_3).setWidth(480);
  _mc(form, '2-3.  In a Q-table heatmap for a maze, cells near the goal show strong consistent colors. Cells far from the goal show weak or mixed colors. What does this indicate?',
    ['A.  The goal area has a higher reward in all directions',
     'B.  The agent has visited cells near the goal more and is more confident there',
     'C.  The agent avoids cells far from the goal',
     'D.  The maze is more complex near the goal'], 1);
}

// ═══════════════════════════════════════════════════════════
// LOW-LEVEL HELPERS
// ═══════════════════════════════════════════════════════════

function _mc(form, title, choices, correctIdx) {
  var item = form.addMultipleChoiceItem();
  item.setTitle(title);
  item.setChoices(choices.map(function(c, i) {
    return item.createChoice(c, i === correctIdx);
  }));
  item.setRequired(true);
  item.setPoints(1);
}

function _likert5(form, title) {
  form.addScaleItem()
    .setTitle(title)
    .setBounds(1, 5)
    .setLabels('Strongly Disagree', 'Strongly Agree')
    .setRequired(true);
}

function _scale10(form, title) {
  form.addScaleItem()
    .setTitle(title)
    .setBounds(1, 10)
    .setLabels('Very Low', 'Very High')
    .setRequired(true);
}
