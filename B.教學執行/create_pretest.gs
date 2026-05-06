/**
 * RL Lab — Pre-Test Form Generator
 *
 * 使用方式：
 *   1. 開啟 script.google.com，建立新專案
 *   2. 貼上本程式碼，執行 createPreTest()
 *   3. 授權後 Form 自動建立，執行記錄會印出連結
 *
 * ⚠️ Section 2 的圖表題建立後需手動插入圖片（3 張）
 */

function createPreTest() {
  var form = FormApp.create('RL Lab — Pre-Test');
  form.setDescription(
    'This form is for research data collection only and does NOT affect your course grade.\n' +
    'Estimated time: ~15 minutes.\n\n' +
    'Please enter the correct Student ID — it is used to match your pre-test and post-test responses for anonymous analysis.'
  );
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage('Thank you! Your pre-test response has been recorded.');

  // ── Helpers ────────────────────────────────────────────────
  function mc(title, choices, correctIdx) {
    var item = form.addMultipleChoiceItem();
    item.setTitle(title);
    item.setChoices(choices.map(function(c, i) {
      return item.createChoice(c, i === correctIdx);
    }));
    item.setRequired(true);
    item.setPoints(1);
  }

  // ── Section 0: Basic Information ───────────────────────────
  form.addTextItem()
    .setTitle('Student ID')
    .setHelpText('Enter your anonymous code (e.g., CS1-23). You will use the same ID in the post-test.')
    .setRequired(true);

  var grpItem = form.addMultipleChoiceItem();
  grpItem.setTitle('Your group');
  grpItem.setChoiceValues(['Group A — RR Platform', 'Group B — Colab']);
  grpItem.setRequired(true);

  var yrItem = form.addMultipleChoiceItem();
  yrItem.setTitle('Year of study');
  yrItem.setChoiceValues(['1st year', '2nd year', '3rd year', '4th year', 'Graduate or above']);
  yrItem.setRequired(true);

  var progItem = form.addMultipleChoiceItem();
  progItem.setTitle('Programming experience');
  progItem.setChoiceValues([
    'None',
    'Basic (< 6 months)',
    'Intermediate (6–12 months)',
    'Advanced (> 1 year)'
  ]);
  progItem.setRequired(true);

  var rlItem = form.addMultipleChoiceItem();
  rlItem.setTitle('Prior knowledge of reinforcement learning');
  rlItem.setChoiceValues([
    'Never heard of it',
    'Heard of it but don\'t understand',
    'Some understanding',
    'Familiar with it'
  ]);
  rlItem.setRequired(true);

  // ── Section 1: RL Concept Questions ────────────────────────
  form.addPageBreakItem()
    .setTitle('Section 1: RL Concept Questions')
    .setHelpText('Choose the best answer for each question.  (5 questions · 1 pt each)');

  mc('1-1.  In reinforcement learning, what does "state" refer to?',
    ['A.  The action taken by the agent',
     'B.  The current observation of the environment',
     'C.  The reward received',
     'D.  The learning rate'], 1);

  mc('1-2.  What happens at the start of a new "episode"?',
    ['A.  The agent receives a large reward',
     'B.  The Q-table is cleared',
     'C.  The environment resets to the initial condition',
     'D.  The agent stops exploring'], 2);

  mc('1-3.  In an ε-greedy strategy, what does a HIGH ε value mean?',
    ['A.  The agent always picks the best known action',
     'B.  The agent explores more randomly',
     'C.  The agent learns faster',
     'D.  The agent ignores all rewards'], 1);

  mc('1-4.  Which of the following best describes what Q(s, a) represents?',
    ['A.  The probability of choosing action a from state s',
     'B.  The immediate reward for taking action a',
     'C.  The expected future reward when taking action a from state s',
     'D.  The number of times action a was taken'], 2);

  mc('1-5.  If an agent always picks the action with the highest Q-value and never tries anything new, what problem might occur?',
    ['A.  The agent learns too slowly',
     'B.  The agent might miss a better action it has never tried',
     'C.  The Q-table grows too large',
     'D.  The reward curve becomes too smooth'], 1);

  // ── Section 2: Chart Interpretation ────────────────────────
  form.addPageBreakItem()
    .setTitle('Section 2: Chart Interpretation')
    .setHelpText(
      '⚠️  Each question is accompanied by a chart.\n' +
      'After this form is created, open the form editor and manually insert the chart image above each question.\n\n' +
      '(3 questions · 1 pt each)'
    );

  mc('2-1.  [Insert chart here]\n\nA reward curve stays flat for the first 100 episodes, then steadily increases. What does this most likely indicate?',
    ['A.  The agent stopped exploring after episode 100',
     'B.  The agent began learning effectively around episode 100',
     'C.  The reward function changed at episode 100',
     'D.  The agent reached the maximum possible reward'], 1);

  mc('2-2.  [Insert chart here]\n\nTwo reward curves are shown: Curve A rises quickly but is noisy and unstable. Curve B rises slowly but is smooth and steady. Which statement is most likely correct?',
    ['A.  Curve A has a lower learning rate than Curve B',
     'B.  Curve A has a higher learning rate than Curve B',
     'C.  Curve B has a higher exploration rate than Curve A',
     'D.  Both curves used the same parameters'], 1);

  mc('2-3.  [Insert chart here]\n\nIn a Q-table heatmap for a maze, cells near the goal show strong, consistent colors. Cells far from the goal show weak or mixed colors. What does this indicate?',
    ['A.  The goal area has a higher reward in all directions',
     'B.  The agent has visited cells near the goal more and is more confident there',
     'C.  The agent avoids cells far from the goal',
     'D.  The maze is more complex near the goal'], 1);

  // ── Done ───────────────────────────────────────────────────
  Logger.log('✅  Pre-test created successfully!');
  Logger.log('📝  Edit URL  : ' + form.getEditUrl());
  Logger.log('🔗  Share URL : ' + form.getPublishedUrl());
}
