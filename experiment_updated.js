(async function() {
  const FEEDBACK_MESSAGES = {
    harsh: "«Вы не прошли тест. Такой результат значительно ниже ожидаемого уровня и свидетельствует о том, что задание было выполнено без должного внимания и усилий. Невнимательное выполнение задания подрывает общий результат и ставит под сомнение вашу ответственность при выполнении задания.»",
    supportive: "«К сожалению, вы не получили желаемую оценку за это задание. Понимаем, что результаты подобных тестов могут различаться по разным причинам и иногда вызывать неприятные ощущения. Однако один показатель сам по себе не отражает ваших общих способностей или приложенных усилий.»"
  };

  function randomChoice(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  const assignedFeedbackCondition = randomChoice(['harsh', 'supportive']);
  const assignedFeedbackText = FEEDBACK_MESSAGES[assignedFeedbackCondition];

  const jsPsych = initJsPsych({
    show_progress_bar: false,
    auto_update_progress_bar: false,
    on_finish: function() {
      const pid = jsPsych.data.get().values()[0]?.participant_id || jsPsych.data.get().filter({trial_type: 'survey-html-form'}).last(1).values()[0]?.response?.participant_id || '001';
      const stamp = new Date().toISOString().replace(/[:.]/g, '-');
      const csv = jsPsych.data.get().csv();
      downloadText(`${pid}_attractive_${stamp}.csv`, csv, 'text/csv');

      document.body.innerHTML = `
        <div class="jspsych-content" style="max-width:900px; margin:60px auto; font-family:Arial,sans-serif; text-align:center;">
          <h2>Эксперимент завершён</h2>
          <p>Файл с данными был скачан на это устройство.</p>
          <p><strong>Важно:</strong> GitHub Pages сам по себе не сохраняет данные в папку репозитория, потому что это статический хостинг.</p>
        </div>`;
    }
  });

  function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    return {
      participant_id: params.get('participant_id') || '',
      age: params.get('age') || '',
      sex: params.get('sex') || '',
      condition: params.get('condition') || ''
    };
  }

  const incoming = getUrlParams();

  function instructionBlock(text) {
    return `
      <div style="max-width:880px; margin:0 auto; font-family:Arial,sans-serif; color:black; text-align:left; line-height:1.6; font-size:20px;">
        ${text}
      </div>`;
  }

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
        <p>Put <code>index.html</code>, <code>experiment_updated.js</code>, <code>practicepics.xlsx</code>, <code>pics.xlsx</code>, and your image files in the same folder.</p>
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
        feedback_condition: assignedFeedbackCondition,
        feedback_text: assignedFeedbackText
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
          feedback_condition: assignedFeedbackCondition,
          feedback_text: assignedFeedbackText
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

  const practiceProcedure = {
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
  };
  timeline.push(practiceProcedure);

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
    stimulus: function() {
      return instructionBlock(`
        <div style="text-align:center; font-size:28px; font-weight:700; margin-bottom:24px;">Оценка выполненного задания</div>
        <p style="font-size:24px; line-height:1.6;">${assignedFeedbackText}</p>
        <p style="margin-top:28px; text-align:center;"><strong>Нажмите пробел, чтобы продолжить.</strong></p>
      `);
    },
    choices: [' '],
    data: {
      phase: 'feedback_message',
      feedback_condition: assignedFeedbackCondition,
      feedback_text: assignedFeedbackText
    }
  });

  timeline.push({
    type: jsPsychSurveyHtmlForm,
    preamble: '<h3>Короткий опрос</h3>',
    html: `
      <div style="max-width:850px; margin:0 auto; text-align:left; font-family:Arial,sans-serif; line-height:1.6;">
        <p><label><strong>Насколько вы согласны с данной оценкой?</strong><br>
        <select name="agreement_with_assessment" required>
          <option value="" selected disabled>Выберите ответ</option>
          <option value="1">1 — совсем не согласен(на)</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
          <option value="6">6</option>
          <option value="7">7 — полностью согласен(на)</option>
        </select></label></p>

        <p><label><strong>Насколько эта оценка показалась вам справедливой?</strong><br>
        <select name="fairness_of_assessment" required>
          <option value="" selected disabled>Выберите ответ</option>
          <option value="1">1 — совсем не справедливой</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
          <option value="6">6</option>
          <option value="7">7 — полностью справедливой</option>
        </select></label></p>

        <p><label><strong>Насколько неприятной для вас была эта оценка?</strong><br>
        <select name="negativity_of_assessment" required>
          <option value="" selected disabled>Выберите ответ</option>
          <option value="1">1 — совсем не неприятной</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
          <option value="6">6</option>
          <option value="7">7 — очень неприятной</option>
        </select></label></p>
      </div>
    `,
    button_label: 'Продолжить',
    data: {
      phase: 'feedback_evaluation',
      feedback_condition: assignedFeedbackCondition,
      feedback_text: assignedFeedbackText
    },
    on_finish: function(data) {
      data.agreement_with_assessment = Number(data.response.agreement_with_assessment || '');
      data.fairness_of_assessment = Number(data.response.fairness_of_assessment || '');
      data.negativity_of_assessment = Number(data.response.negativity_of_assessment || '');
    }
  });

  timeline.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<div class="center-big">+</div>',
    choices: 'NO_KEYS',
    trial_duration: 1000,
    data: { phase: 'fixation_before_main' }
  });

  const mainProcedure = {
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
  };
  timeline.push(mainProcedure);

  timeline.push({
    type: jsPsychSurveyHtmlForm,
    preamble: '<h3>Завершение</h3>',
    html: `
      <div style="max-width:850px; margin:0 auto; text-align:left; font-family:Arial,sans-serif; line-height:1.6;">
        <p><label><strong>Как вы думаете, какова была цель этого исследования?</strong><br>
        <textarea name="study_goal_guess" rows="4" cols="70"></textarea></label></p>

        <p><label><strong>Как вы думаете, использовалось ли в исследовании какое-либо скрытое влияние, обман или введение в заблуждение?</strong><br>
        <select name="suspected_deception" required>
          <option value="" selected disabled>Выберите ответ</option>
          <option value="no">Нет</option>
          <option value="maybe">Не уверен(а)</option>
          <option value="yes">Да</option>
        </select></label></p>

        <p><label><strong>Если да или если у вас есть догадка, опишите, в чём именно это могло заключаться.</strong><br>
        <textarea name="deception_guess_text" rows="4" cols="70"></textarea></label></p>

        <p><label><strong>Замечали ли вы что-то необычное в ходе эксперимента?</strong><br>
        <textarea name="unusual_noticed" rows="3" cols="70"></textarea></label></p>

        <p><label><strong>Комментарий (необязательно):</strong><br>
        <textarea name="final_comment" rows="3" cols="70"></textarea></label></p>
      </div>
    `,
    button_label: 'Завершить',
    data: { phase: 'suspicion_probe' },
    on_finish: function(data) {
      data.study_goal_guess = data.response.study_goal_guess || '';
      data.suspected_deception = data.response.suspected_deception || '';
      data.deception_guess_text = data.response.deception_guess_text || '';
      data.unusual_noticed = data.response.unusual_noticed || '';
      data.final_comment = data.response.final_comment || '';
    }
  });

  timeline.push({
    type: jsPsychFullscreen,
    fullscreen_mode: false,
    delay_after: 0
  });

  jsPsych.run(timeline);
})();
