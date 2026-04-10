
(async function() {
  let dataAlreadySaved = false;

  function downloadText(filename, text, mimeType) {
    const blob = new Blob([text], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function attemptCloseWindow() {
    try { window.open('', '_self'); } catch (e) {}
    try { window.close(); } catch (e) {}
    setTimeout(function() {
      document.body.innerHTML = '';
      try { window.location.replace('about:blank'); } catch (e) {}
    }, 150);
  }

  const jsPsych = initJsPsych({
    show_progress_bar: false,
    auto_update_progress_bar: false,
    on_finish: function() {
      attemptCloseWindow();
    }
  });

  function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    return {
      participant_id: params.get('participant_id') || '',
      age: params.get('age') || '',
      sex: params.get('sex') || '',
      condition: params.get('c') || params.get('condition') || ''
    };
  }

  const incoming = getUrlParams();

  function instructionBlock(text) {
    return `
      <div style="max-width:880px; margin:0 auto; font-family:Arial,sans-serif; color:black; text-align:left; line-height:1.6; font-size:20px;">
        ${text}
      </div>`;
  }

  async function loadWorkbookRows(filename) {
    const response = await fetch(filename, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error(`Could not load ${filename} (HTTP ${response.status})`);
    }
    const arrayBuffer = await response.arrayBuffer();
    const workbook = XLSX.read(arrayBuffer, { type: 'array' });
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    return XLSX.utils.sheet_to_json(sheet, { defval: '' });
  }

  function normalizeTrialRow(row) {
    const normalized = {};
    for (const [key, value] of Object.entries(row)) {
      normalized[String(key).trim().toLowerCase()] = value;
    }
    return normalized;
  }

  function firstExisting(row, keys, fallback = '') {
    for (const key of keys) {
      if (row[key] !== undefined && row[key] !== null && String(row[key]).trim() !== '') {
        return row[key];
      }
    }
    return fallback;
  }

  function buildPracticeTrials(rows) {
    return rows.map((raw, index) => {
      const row = normalizeTrialRow(raw);
      const image = firstExisting(row, ['pra', 'practiceimage', 'image', 'img', 'stimulus']);
      if (!image) {
        throw new Error(`practicepics.xlsx row ${index + 2} has no image column. Expected something like 'pra'.`);
      }
      const majority = Number(firstExisting(row, ['picked', 'majority', 'rating', 'consensus'], NaN));
      const percent = firstExisting(row, ['percent', 'percentage', 'perc', 'share'], '');
      return {
        phase: 'practice',
        stimulus_image: String(image).trim(),
        majority_rating: Number.isFinite(majority) ? majority : randomChoice([3, 4, 6, 7]),
        majority_percent: percent === '' ? '' : String(percent).trim()
      };
    });
  }

  function buildMainTrials(rows) {
    return rows.map((raw, index) => {
      const row = normalizeTrialRow(raw);
      const image = firstExisting(row, ['target', 'image', 'img', 'stimulus']);
      if (!image) {
        throw new Error(`pics.xlsx row ${index + 2} has no image column. Expected something like 'target'.`);
      }
      const majority = Number(firstExisting(row, ['picked', 'majority', 'rating', 'consensus'], NaN));
      const percent = firstExisting(row, ['percent', 'percentage', 'perc', 'share'], '');
      return {
        phase: 'main',
        stimulus_image: String(image).trim(),
        majority_rating: Number.isFinite(majority) ? majority : randomChoice([3, 4, 6, 7]),
        majority_percent: percent === '' ? '' : String(percent).trim()
      };
    });
  }

  function randomChoice(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function shuffle(arr) {
    return jsPsych.randomization.shuffle(arr.slice());
  }

  function ratingHtml(majorityRating, majorityPercent) {
    const cells = Array.from({ length: 9 }, (_, i) => {
      const value = i + 1;
      const cls = value === Number(majorityRating) ? 'scale-cell highlight' : 'scale-cell';
      return `<div class="${cls}">${value}</div>`;
    }).join('');

    const majorityText = majorityPercent
      ? `${majorityRating} (${majorityPercent}%)`
      : `${majorityRating}`;

    return `
      <div class="rating-wrap">
        <div class="majority-row">${majorityText}</div>
        <div class="scale-row">${cells}</div>
        <div class="response-hint">Нажмите цифру от <strong>1</strong> до <strong>9</strong>.</div>
      </div>`;
  }

  const feedbackPool = [
    {
      feedback_condition: 'negative_controlling',
      feedback_text: 'Вы не прошли тест. Такой результат значительно ниже ожидаемого уровня и свидетельствует о том, что задание было выполнено без должного внимания и усилий. Невнимательное выполнение задания подрывает общий результат и ставит под сомнение вашу ответственность при выполнении задания.'
    },
    {
      feedback_condition: 'negative_supportive',
      feedback_text: 'К сожалению, вы не получили желаемую оценку за это задание. Понимаем, что результаты подобных тестов могут различаться по разным причинам и иногда вызывать неприятные ощущения. Однако один показатель сам по себе не отражает ваших общих способностей или приложенных усилий.'
    }
  ];

  const assignedFeedback = randomChoice(feedbackPool);

  let practiceRows = [];
  let mainRows = [];
  try {
    [practiceRows, mainRows] = await Promise.all([
      loadWorkbookRows('practicepics.xlsx'),
      loadWorkbookRows('pics.xlsx')
    ]);
  } catch (err) {
    document.body.innerHTML = `
      <div style="max-width:900px; margin:60px auto; font-family:Arial,sans-serif;">
        <h2>Loading error</h2>
        <p>${String(err.message)}</p>
        <p>Put <code>index_combined.html</code>, <code>experiment_updated.js</code>, <code>practicepics.xlsx</code>, <code>pics.xlsx</code>, and your image files in the same folder.</p>
      </div>`;
    throw err;
  }

  const practiceTrials = shuffle(buildPracticeTrials(practiceRows));
  const mainTrials = shuffle(buildMainTrials(mainRows));
  const imageFiles = [...new Set([...practiceTrials, ...mainTrials].map(t => t.stimulus_image))];

  const timeline = [];

  timeline.push({
    type: jsPsychBrowserCheck,
    inclusion_function: (data) => ['chrome', 'firefox', 'safari', 'edge'].includes((data.browser || '').toLowerCase()),
    exclusion_message: () => '<p>Please run this experiment in a recent version of Chrome, Firefox, Safari, or Edge.</p>'
  });

  timeline.push({
    type: jsPsychPreload,
    images: imageFiles,
    message: '<p>Loading, please wait…</p>',
    continue_after_error: false,
    show_detailed_errors: true
  });

  timeline.push({
    type: jsPsychCallFunction,
    func: function() {
      jsPsych.data.addProperties({
        participant_id: incoming.participant_id || '001',
        age: incoming.age || '',
        sex: incoming.sex || '',
        upstream_condition: incoming.condition || '',
        feedback_condition: assignedFeedback.feedback_condition,
        feedback_text: assignedFeedback.feedback_text
      });
    }
  });

  if (!(incoming.participant_id || incoming.age || incoming.sex)) {
    timeline.push({
      type: jsPsychSurveyHtmlForm,
      preamble: '<h3>Данные участника</h3>',
      html: `
        <p><label>Пол (1-М, 2-Ж): <input name="sex" required></label></p>
        <p><label>Возраст: <input name="age" required></label></p>
        <p><label>Номер участника: <input name="participant_id" value="001" required></label></p>
      `,
      button_label: 'Продолжить',
      on_finish: function(data) {
        jsPsych.data.addProperties({
          participant_id: data.response.participant_id || '001',
          age: data.response.age || '',
          sex: data.response.sex || '',
          upstream_condition: incoming.condition || '',
          feedback_condition: assignedFeedback.feedback_condition,
          feedback_text: assignedFeedback.feedback_text
        });
      }
    });
  }

  timeline.push({
    type: jsPsychFullscreen,
    fullscreen_mode: true,
    message: '<p>Эксперимент перейдёт в полноэкранный режим.</p>',
    button_label: 'Начать'
  });

  timeline.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: instructionBlock(`
      <div style="text-align:center; font-size:30px; font-weight:700; margin-bottom:26px;">Добро пожаловать!</div>
      <p>В этом эксперименте вам нужно будет оценивать привлекательность лиц.</p>
      <p>Сначала в центре экрана появится лицо.</p>
      <p>После того как лицо исчезнет, в центре экрана будет показана оценка других участников.</p>
      <p>Зелёный квадрат показывает, какую оценку поставило большинство других участников.</p>
      <p>Вам нужно оценить лицо по шкале от 1 (очень непривлекательно) до 9 (очень привлекательно).</p>
      <p>Пожалуйста, старайтесь давать оценку как можно быстрее, не раздумывая слишком долго.</p>
      <p>Во время эксперимента постарайтесь держать взгляд направленным в центр экрана.</p>
      <p>Сначала мы проведём короткую тренировочную серию, чтобы показать, как будет проходить эксперимент.</p>
      <p style="margin-top:28px; text-align:center;"><strong>Если вы готовы, нажмите пробел, чтобы начать.</strong></p>
    `),
    choices: [' '],
    data: { phase: 'instructions_1' }
  });

  timeline.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<div class="center-big">+</div>',
    choices: 'NO_KEYS',
    trial_duration: 1000,
    data: { phase: 'fixation_before_practice' }
  });

  timeline.push({
    timeline: [
      {
        type: jsPsychImageKeyboardResponse,
        stimulus: jsPsych.timelineVariable('stimulus_image'),
        choices: 'NO_KEYS',
        trial_duration: 1000,
        stimulus_height: 320,
        maintain_aspect_ratio: true,
        render_on_canvas: false,
        data: {
          phase: 'practice_image',
          stimulus_image: jsPsych.timelineVariable('stimulus_image')
        }
      },
      {
        type: jsPsychHtmlKeyboardResponse,
        stimulus: function() {
          return ratingHtml(
            jsPsych.evaluateTimelineVariable('majority_rating'),
            jsPsych.evaluateTimelineVariable('majority_percent')
          );
        },
        choices: ['1','2','3','4','5','6','7','8','9'],
        data: {
          phase: 'practice_rating',
          stimulus_image: jsPsych.timelineVariable('stimulus_image'),
          majority_rating: jsPsych.timelineVariable('majority_rating'),
          majority_percent: jsPsych.timelineVariable('majority_percent')
        },
        on_finish: function(data) {
          data.rating = Number(data.response);
        }
      }
    ],
    timeline_variables: practiceTrials,
    randomize_order: false
  });

  timeline.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: instructionBlock(`
      <div style="text-align:center; font-size:28px; font-weight:700; margin-bottom:24px;">Тренировочная часть завершена.</div>
      <p>Если вам всё ещё не совсем понятно, что нужно делать, пожалуйста, сообщите об этом экспериментатору.</p>
      <p>Если всё понятно, пожалуйста, прочитайте следующее:</p>
      <p>Работа, которую вы выполнили 5 минут назад, была оценена руководителем проекта.</p>
      <p>Он(а) даст своё личное и честное мнение о выполненной вами работе.</p>
      <p>Вам не нужно ничего делать с этим отзывом, кроме как внимательно его прочитать.</p>
      <p>После того как вы его прочитаете, вы продолжите остальную часть эксперимента.</p>
      <p style="margin-top:28px; text-align:center;"><strong>Если всё понятно и вы готовы прочитать отзыв, пожалуйста, нажмите ПРОБЕЛ.</strong></p>
    `),
    choices: [' '],
    data: { phase: 'instructions_2' }
  });

  timeline.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: instructionBlock(`
      <div style="max-width:900px; margin:0 auto;">
        <div style="text-align:center; font-size:30px; font-weight:700; margin-bottom:26px;">Оценка выполненного задания</div>
        <p style="font-size:24px; line-height:1.6;">${assignedFeedback.feedback_text}</p>
        <p style="margin-top:28px; text-align:center;"><strong>Нажмите пробел, чтобы продолжить.</strong></p>
      </div>
    `),
    choices: [' '],
    data: {
      phase: 'feedback_message',
      feedback_condition: assignedFeedback.feedback_condition,
      feedback_text: assignedFeedback.feedback_text
    }
  });

  timeline.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<div class="center-big">+</div>',
    choices: 'NO_KEYS',
    trial_duration: 1000,
    data: { phase: 'fixation_before_main' }
  });

  timeline.push({
    timeline: [
      {
        type: jsPsychImageKeyboardResponse,
        stimulus: jsPsych.timelineVariable('stimulus_image'),
        choices: 'NO_KEYS',
        trial_duration: 1000,
        stimulus_height: 320,
        maintain_aspect_ratio: true,
        render_on_canvas: false,
        data: {
          phase: 'main_image',
          stimulus_image: jsPsych.timelineVariable('stimulus_image')
        }
      },
      {
        type: jsPsychHtmlKeyboardResponse,
        stimulus: function() {
          return ratingHtml(
            jsPsych.evaluateTimelineVariable('majority_rating'),
            jsPsych.evaluateTimelineVariable('majority_percent')
          );
        },
        choices: ['1','2','3','4','5','6','7','8','9'],
        data: {
          phase: 'main_rating',
          stimulus_image: jsPsych.timelineVariable('stimulus_image'),
          majority_rating: jsPsych.timelineVariable('majority_rating'),
          majority_percent: jsPsych.timelineVariable('majority_percent')
        },
        on_finish: function(data) {
          data.rating = Number(data.response);
        }
      }
    ],
    timeline_variables: mainTrials,
    randomize_order: false
  });

  timeline.push({
    type: jsPsychSurveyLikert,
    preamble: '<h3>Несколько вопросов о только что увиденной обратной связи</h3><p>Пожалуйста, оцените, насколько вы согласны со следующими утверждениями.</p>',
    questions: [
      {
        prompt: 'Я согласен(согласна) с данной оценкой.',
        labels: ['Совершенно не согласен(на)', 'Скорее не согласен(на)', 'Ни то ни другое', 'Скорее согласен(на)', 'Полностью согласен(на)'],
        required: true
      },
      {
        prompt: 'Эта оценка показалась мне справедливой.',
        labels: ['Совершенно не согласен(на)', 'Скорее не согласен(на)', 'Ни то ни другое', 'Скорее согласен(на)', 'Полностью согласен(на)'],
        required: true
      },
      {
        prompt: 'Это сообщение вызвало у меня неприятные ощущения.',
        labels: ['Совершенно не согласен(на)', 'Скорее не согласен(на)', 'Ни то ни другое', 'Скорее согласен(на)', 'Полностью согласен(на)'],
        required: true
      }
    ],
    button_label: 'Продолжить',
    data: {
      phase: 'post_task_feedback_questionnaire',
      feedback_condition: assignedFeedback.feedback_condition
    },
    on_finish: function(data) {
      const r = data.response || {};
      data.agree_with_assessment = (r.Q0 ?? null) !== null ? Number(r.Q0) + 1 : null;
      data.assessment_fairness = (r.Q1 ?? null) !== null ? Number(r.Q1) + 1 : null;
      data.assessment_unpleasant = (r.Q2 ?? null) !== null ? Number(r.Q2) + 1 : null;
    }
  });

  timeline.push({
    type: jsPsychSurveyHtmlForm,
    preamble: '<h3>Несколько завершающих вопросов</h3><p>Пожалуйста, ответьте максимально честно.</p>',
    html: `
      <p><label>Как вы думаете, какова была настоящая цель исследования?<br><textarea name="study_goal_guess" rows="4" cols="70" required></textarea></label></p>
      <p><label>Было ли у вас ощущение, что в исследовании использовалась не полностью точная информация или скрытая часть процедуры?<br>
        <select name="suspected_deception" required>
          <option value="">Выберите ответ</option>
          <option value="no">Нет</option>
          <option value="yes">Да</option>
          <option value="unsure">Не уверен(а)</option>
        </select></label></p>
      <p><label>Если да или если у вас были подозрения, напишите, в чём, по вашему мнению, это заключалось.<br><textarea name="deception_guess" rows="4" cols="70"></textarea></label></p>
      <p><label>Было ли что-то необычное или вызывающее сомнение в ходе исследования?<br><textarea name="unusual_noticed" rows="4" cols="70"></textarea></label></p>
      <p><label>Дополнительный комментарий (необязательно).<br><textarea name="final_comment" rows="4" cols="70"></textarea></label></p>
    `,
    button_label: 'Продолжить',
    data: { phase: 'suspicion_probe' }
  });

  timeline.push({
    type: jsPsychCallFunction,
    func: function() {
      if (dataAlreadySaved) return;
      const pid = jsPsych.data.get().values()[0]?.participant_id || '001';
      const stamp = new Date().toISOString().replace(/[:.]/g, '-');
      const csv = jsPsych.data.get().csv();
      downloadText(`${pid}_attractive_${stamp}.csv`, csv, 'text/csv');
      dataAlreadySaved = true;
    },
    data: { phase: 'data_saved_before_debrief' }
  });

  timeline.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: instructionBlock(`
      <div style="white-space:pre-line; max-width:900px; margin:0 auto;">
Спасибо за участие в нашем исследовании.

Цель исследования

Цель данного исследования: изучить, как подростки принимают
решения и как реагируют на различные формы социальной информации и
обратной связи.
Чтобы результаты исследования были достоверными, не вся информация
о процедуре исследования сообщалась участникам заранее.

Оценочные сообщения

Во время выполнения математического задания некоторые участники
могли получать сообщения с оценкой результата. Эти сообщения
являлись частью экспериментальной процедуры и не отражали реальный
уровень способностей или усилий участника.
Такая процедура используется в психологических исследованиях для
изучения того, как люди реагируют на различные виды обратной связи.

Ваши данные

Все данные, полученные в ходе исследования, будут обезличены.
Результаты исследования могут быть использованы в научных
публикациях только в обобщённом виде.

Контакт исследователя

Если у вас или у вашего родителя/законного представителя возникли
вопросы о данном исследовании, вы можете связаться с исследователем.

Контакт:
Тотурбиев Бадыр
badyrc@mail.ru
      </div>
      <p style="margin-top:28px; text-align:center;"><strong>Нажмите пробел, чтобы завершить.</strong></p>
    `),
    choices: [' '],
    data: { phase: 'final_debrief' }
  });

  timeline.push({
    type: jsPsychFullscreen,
    fullscreen_mode: false,
    delay_after: 0
  });

  jsPsych.run(timeline);
})();
