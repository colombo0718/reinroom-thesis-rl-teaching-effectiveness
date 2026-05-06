/**
 * RL Lab — Post-Test Form Generator (Group B — Google Colab)
 *
 * 使用方式：
 *   1. 開啟 script.google.com，建立新專案
 *   2. 貼上本程式碼，執行 createPostTestB()
 *   3. 授權後 Form 自動建立，執行記錄會印出連結
 *
 * ⚠️ Section 2 的圖表題建立後需手動插入圖片（3 張，與前測相同）
 */

function createPostTestB() {
  var form = FormApp.create('RL Lab — Post-Test (Group B)');
  form.setDescription(
    'This form is for research data collection only and does NOT affect your course grade.\n' +
    'Estimated time: ~25 minutes.\n\n' +
    'Please enter the same Student ID you used in the pre-test.'
  );
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage('Thank you! Your post-test response has been recorded.');

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

  function likert5(title) {
    form.addScaleItem()
      .setTitle(title)
      .setBounds(1, 5)
      .setLabels('Strongly Disagree', 'Strongly Agree')
      .setRequired(true);
  }

  function scale10(title, lowLabel, highLabel) {
    form.addScaleItem()
      .setTitle(title)
      .setBounds(1, 10)
      .setLabels(lowLabel || 'Very Low', highLabel || 'Very High')
      .setRequired(true);
  }

  // ── Section 0: Basic Information ───────────────────────────
  form.addTextItem()
    .setTitle('Student ID')
    .setHelpText('Enter the same anonymous code you used in the pre-test (e.g., CS1-23).')
    .setRequired(true);

  // ── Section 1: RL Concept Questions (same as pre-test) ─────
  form.addPageBreakItem()
    .setTitle('Section 1: RL Concept Questions')
    .setHelpText('Same questions as the pre-test.  (5 questions · 1 pt each)');

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

  // ── Section 2: Chart Interpretation (same as pre-test) ─────
  form.addPageBreakItem()
    .setTitle('Section 2: Chart Interpretation')
    .setHelpText(
      '⚠️  Each question is accompanied by a chart (same charts as the pre-test).\n' +
      'Please insert the chart image above each question after form creation.\n\n' +
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

  // ── Section 3B: Platform Feedback — Colab ──────────────────
  form.addPageBreakItem()
    .setTitle('Section 3: Platform Experience — Google Colab')
    .setHelpText('Rate each statement from 1 (Strongly Disagree) to 5 (Strongly Agree).  (5 questions)');

  likert5('3-1.  The Colab interface was easy to use.');
  likert5('3-2.  I felt confident modifying the parameters (alpha, gamma, epsilon) in the code.');
  likert5('3-3.  The charts generated by the code helped me understand what the agent was learning.');
  likert5('3-4.  I am interested in learning more about reinforcement learning after this class.');
  likert5('3-5.  I would recommend Colab + the course notebooks to someone who wants to learn about RL.');

  // ── Section 4: NASA-TLX ────────────────────────────────────
  form.addPageBreakItem()
    .setTitle('Section 4: Task Load Index (NASA-TLX)')
    .setHelpText(
      'Please rate each dimension based on your experience during today\'s learning activities.\n' +
      'Use 1 (Very Low) to 10 (Very High).  (6 questions)'
    );

  scale10('4-1.  Mental Demand — How much mental and perceptual activity was required? (thinking, deciding, remembering, etc.)');
  scale10('4-2.  Physical Demand — How much physical activity was required? (clicking, scrolling, typing, etc.)');
  scale10('4-3.  Temporal Demand — How much time pressure did you feel during the tasks?');
  scale10('4-4.  Performance — How successful do you think you were in accomplishing the goals set by the instructor?',
          'Perfect (1)', 'Failure (10)');
  scale10('4-5.  Effort — How hard did you have to work to accomplish your level of performance?');
  scale10('4-6.  Frustration — How insecure, discouraged, irritated, stressed, or annoyed did you feel?');

  // ── Section 5B: SUS — Colab ────────────────────────────────
  form.addPageBreakItem()
    .setTitle('Section 5: System Usability Scale (SUS) — Google Colab')
    .setHelpText('Rate each statement from 1 (Strongly Disagree) to 5 (Strongly Agree).  (10 questions)');

  likert5('5-1.  I think that I would like to use Google Colab with these notebooks frequently.');
  likert5('5-2.  I found the Colab + notebook setup unnecessarily complex.');
  likert5('5-3.  I thought the Colab + notebook setup was easy to use.');
  likert5('5-4.  I think that I would need the support of a technical person to be able to use the Colab notebooks.');
  likert5('5-5.  I found the various parts of the Colab notebooks were well integrated.');
  likert5('5-6.  I thought there was too much inconsistency in how the Colab notebooks worked.');
  likert5('5-7.  I would imagine that most people would learn to use these Colab notebooks very quickly.');
  likert5('5-8.  I found the Colab + notebook setup very cumbersome to use.');
  likert5('5-9.  I felt very confident using Google Colab for this course.');
  likert5('5-10.  I needed to learn a lot of things before I could get going with the Colab notebooks.');

  // ── Section 6: Open Feedback ───────────────────────────────
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

  // ── Done ───────────────────────────────────────────────────
  Logger.log('✅  Post-test Group B created successfully!');
  Logger.log('📝  Edit URL  : ' + form.getEditUrl());
  Logger.log('🔗  Share URL : ' + form.getPublishedUrl());
}
