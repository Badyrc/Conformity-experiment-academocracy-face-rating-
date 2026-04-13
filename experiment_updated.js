
(async function() {
  const RESPONSES_REQUIRED = false;
  const SUSPICION_SELECT_REQUIRED = false;

  const FEEDBACK_MESSAGES = [
    {
      key: 'negative_harsh',
      text: '«Вы не прошли тест. Такой результат значительно ниже ожидаемого уровня и свидетельствует о том, что задание было выполнено без должного внимания и усилий. Невнимательное выполнение задания подрывает общий результат и ставит под сомнение вашу ответственность при выполнении задания.»'
    },
    {
      key: 'negative_supportive',
      text: '«К сожалению, вы не получили желаемую оценку за это задание. Понимаем, что результаты подобных тестов могут различаться по разным причинам и иногда вызывать неприятные ощущения. Однако один показатель сам по себе не отражает ваших общих способностей или приложенных усилий.»'
    }
  ];

  let assignedFeedback = FEEDBACK_MESSAGES[Math.floor(Math.random() * FEEDBACK_MESSAGES.length)];
  const WEB3FORMS_ACCESS_KEY = 'd5801e60-32a6-40aa-82b8-b546db2d91d6';

  const jsPsych = initJsPsych({
    show_progress_bar: false,
    auto_update_progress_bar: false
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

  const GOOGLE_SHEETS_WEB_APP_URL = 'PASTE_YOUR_CURRENT_GOOGLE_APPS_SCRIPT_WEB_APP_URL_HERE';

  function safeJsonParse(value, fallback = {}) {
    try {
      return typeof value === 'string' ? JSON.parse(value) : (value || fallback);
    } catch (e) {
      return fallback;
    }
  }

  function postPayloadToGoogleSheets(payload) {
    const body = JSON.stringify(payload);

    try {
      if (navigator.sendBeacon) {
        const blob = new Blob([body], { type: 'text/plain;charset=UTF-8' });
        const beaconSent = navigator.sendBeacon(GOOGLE_SHEETS_WEB_APP_URL, blob);
        if (beaconSent) {
          return Promise.resolve({ sent: true, transport: 'beacon' });
        }
      }
    } catch (e) {}

    return fetch(GOOGLE_SHEETS_WEB_APP_URL, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'text/plain;charset=UTF-8' },
      body,
      keepalive: true,
      credentials: 'omit'
    }).then(() => ({ sent: true, transport: 'fetch' }));
  }

  function buildStage2FormattedRow() {
    const trials = jsPsych.data.get().values();
    const first = trials[0] || {};
    const row = {
      participant_id: first.participant_id || incoming.participant_id || '',
      stage: 'stage2',
      age: first.age || incoming.age || '',
      sex: first.sex || incoming.sex || '',
      upstream_condition: first.upstream_condition || incoming.condition || '',
      feedback_condition: first.feedback_condition || assignedFeedback.key,
      feedback_text: first.feedback_text || assignedFeedback.text
    };

    const messageQuestionnaire = trials.find(t => t.phase === 'message_questionnaire');
    if (messageQuestionnaire) {
      const resp = safeJsonParse(messageQuestionnaire.response, safeJsonParse(messageQuestionnaire.responses, {}));
      row.agree_assessment = resp.agree_assessment || '';
      row.fairness_message = resp.fairness_message || '';
      row.message_unpleasant = resp.message_unpleasant || '';
    }

    const suspicionQuestionnaire = trials.find(t => t.phase === 'suspicion_questionnaire');
    if (suspicionQuestionnaire) {
      const resp = safeJsonParse(suspicionQuestionnaire.response, safeJsonParse(suspicionQuestionnaire.responses, {}));
      row.study_guess = resp.study_guess || '';
      row.suspected_deception = resp.suspected_deception || '';
      row.deception_guess = resp.deception_guess || '';
      row.unusual_notes = resp.unusual_notes || '';
      row.final_comment = resp.final_comment || '';
    }

    const breakTrial = trials.find(t => t.phase === 'break_firefly');
    if (breakTrial) {
      row.break_score = breakTrial.break_score || '';
      row.break_duration_seconds = breakTrial.break_duration_seconds || '';
    }

    const mainRatings = trials.filter(t => t.phase === 'main_rating');
    mainRatings.forEach((trial, index) => {
      const n = index + 1;
      row['face_' + n + '_stimulus'] = trial.stimulus_image || '';
      row['face_' + n + '_majority_rating'] = trial.majority_rating || '';
      row['face_' + n + '_chosen_rating'] = trial.rating || trial.response || '';
    });

    return row;
  }

  function sendStage2DataToGoogleSheets() {
    const allRows = jsPsych.data.get().values();
    return postPayloadToGoogleSheets({
      stage: 'stage2',
      participant_id: allRows[0] && allRows[0].participant_id ? allRows[0].participant_id : (incoming.participant_id || ''),
      age: allRows[0] && allRows[0].age ? allRows[0].age : (incoming.age || ''),
      sex: allRows[0] && allRows[0].sex ? allRows[0].sex : (incoming.sex || ''),
      condition: allRows[0] && allRows[0].upstream_condition ? allRows[0].upstream_condition : (incoming.condition || ''),
      raw_rows: allRows,
      formatted_row: buildStage2FormattedRow()
    });
  }

  function withTimeout(promise, ms) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('timeout')), ms);
      promise.then(
        value => {
          clearTimeout(timer);
          resolve(value);
        },
        err => {
          clearTimeout(timer);
          reject(err);
        }
      );
    });
  }

  function showSavingScreen() {
    const display = jsPsych.getDisplayElement();
    if (!display) return;
    display.innerHTML = `
      <div style="max-width:820px; margin:60px auto; font-family:Arial,sans-serif; text-align:center; color:black; line-height:1.6;">
        <h2 style="margin-bottom:18px;">Сохранение ответов</h2>
        <p style="font-size:20px;">Пожалуйста, подождите. Затем автоматически откроется заключительный экран.</p>
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

  if (incoming.participant_id || incoming.age || incoming.sex) {
    timeline.push({
      type: jsPsychCallFunction,
      func: function() {
        jsPsych.data.addProperties({
          participant_id: incoming.participant_id || '001',
          age: incoming.age || '',
          sex: incoming.sex || '',
          upstream_condition: incoming.condition || '',
          feedback_condition: assignedFeedback.key,
          feedback_text: assignedFeedback.text
        });
      }
    });
  } else {
    timeline.push({
      type: jsPsychSurveyHtmlForm,
      preamble: '<h3>Данные участника</h3>',
      html: `
        <p><label>Пол (1-М, 2-Ж): <input name="sex"></label></p>
        <p><label>Возраст: <input name="age"></label></p>
        <p><label>Номер участника: <input name="participant_id" value="001"></label></p>
      `,
      button_label: 'Продолжить',
      on_finish: function(data) {
        jsPsych.data.addProperties({
          participant_id: data.response.participant_id || '001',
          age: data.response.age || '',
          sex: data.response.sex || '',
          upstream_condition: incoming.condition || '',
          feedback_condition: assignedFeedback.key,
          feedback_text: assignedFeedback.text
        });
      }
    });
  }

  timeline.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: `
      <div style="max-width:920px; margin:30px auto; font-family:Arial,sans-serif; color:black; text-align:center;">
        <h2 style="margin-bottom:14px;">Небольшой перерыв</h2>
        <p style="font-size:20px; line-height:1.5; max-width:760px; margin:0 auto 16px;">
          Перед началом следующей части исследования, пожалуйста, сделайте 5-минутный перерыв.
        </p>
        <p style="font-size:18px; line-height:1.5; max-width:760px; margin:0 auto 20px;">
          Ниже можно поиграть в спокойную мини-игру: нажимайте на светлячков, когда они появляются на экране.
        </p>
        <div id="breakTimer" style="font-size:28px; font-weight:700; margin-bottom:18px;">05:00</div>
        <canvas id="fireflyCanvas" width="820" height="420" style="max-width:90vw; border:1px solid #ddd; border-radius:14px; background:linear-gradient(180deg,#0e1a2b,#152941);"></canvas>
        <div style="margin-top:16px; color:#f7f3c6;">Поймано светлячков: <span id="fireflyScore">0</span></div>
        <div style="margin-top:20px;">
          <button id="breakContinue" style="display:none; padding:12px 22px; font-size:18px; cursor:pointer;">Продолжить</button>
        </div>
      </div>
    `,
    choices: "NO_KEYS",
    on_load: function() {
      const totalSeconds = 300;
      let remaining = totalSeconds;
      const timerEl = document.getElementById('breakTimer');
      const btn = document.getElementById('breakContinue');
      const canvas = document.getElementById('fireflyCanvas');
      const ctx = canvas.getContext('2d');
      const scoreEl = document.getElementById('fireflyScore');
      let score = 0;
      let active = true;

      const fireflies = Array.from({length: 12}, (_, i) => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: 8 + Math.random() * 7,
        dx: (Math.random() - 0.5) * 0.8,
        dy: (Math.random() - 0.5) * 0.8,
        glow: Math.random() * Math.PI * 2,
        visible: true
      }));

      function formatTime(sec) {
        const m = String(Math.floor(sec / 60)).padStart(2, '0');
        const s = String(sec % 60).padStart(2, '0');
        return `${m}:${s}`;
      }

      function draw() {
        if (!active) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (const f of fireflies) {
          f.x += f.dx;
          f.y += f.dy;
          if (f.x < 10 || f.x > canvas.width - 10) f.dx *= -1;
          if (f.y < 10 || f.y > canvas.height - 10) f.dy *= -1;
          f.glow += 0.05;
          const alpha = 0.45 + 0.35 * Math.sin(f.glow);
          ctx.beginPath();
          ctx.arc(f.x, f.y, f.r * 1.9, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(255, 233, 120, ${Math.max(0.06, alpha * 0.15)})`;
          ctx.fill();
          ctx.beginPath();
          ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(255, 240, 140, ${Math.max(0.4, alpha)})`;
          ctx.fill();
        }
        requestAnimationFrame(draw);
      }

      canvas.addEventListener('click', function(e) {
        if (!active) return;
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        const x = (e.clientX - rect.left) * scaleX;
        const y = (e.clientY - rect.top) * scaleY;
        fireflies.forEach(f => {
          const dist = Math.hypot(f.x - x, f.y - y);
          if (dist <= f.r * 1.6) {
            score += 1;
            scoreEl.textContent = String(score);
            f.x = Math.random() * canvas.width;
            f.y = Math.random() * canvas.height;
            f.dx = (Math.random() - 0.5) * 0.8;
            f.dy = (Math.random() - 0.5) * 0.8;
          }
        });
      });

      timerEl.textContent = formatTime(remaining);
      const interval = setInterval(() => {
        remaining -= 1;
        timerEl.textContent = formatTime(Math.max(0, remaining));
        if (remaining <= 0) {
          clearInterval(interval);
          btn.style.display = 'inline-block';
        }
      }, 1000);

      btn.addEventListener('click', function() {
        active = false;
        clearInterval(interval);
        jsPsych.finishTrial({ break_score: score, break_duration_seconds: totalSeconds });
      });

      draw();
    },
    data: { phase: 'break_firefly' }
  });

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
      <p>В этой части эксперимента вам нужно будет оценивать привлекательность лиц.</p>
      <p>Сначала в центре экрана появится лицо.</p>
      <p>После того как лицо исчезнет, в центре экрана будет показана оценка других участников.</p>
      <p>Зелёный квадрат показывает, какую оценку поставило большинство других участников.</p>
      <p>Вам нужно оценить лицо по шкале от 1 (очень непривлекательно) до 9 (очень привлекательно).</p>
      <p>Пожалуйста, старайтесь давать оценку как можно быстрее, не раздумывая слишком долго.</p>
      <p>Сначала мы проведём короткую тренировочную серию.</p>
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
      <p>Теперь вам будет показана оценка вашего письменного задания, выполненного в первой части исследования.</p>
      <p>Пожалуйста, внимательно прочитайте сообщение на следующем экране.</p>
      <p>После этого вы продолжите основную часть задания.</p>
      <p style="margin-top:28px; text-align:center;"><strong>Нажмите пробел, чтобы продолжить.</strong></p>
    `),
    choices: [' '],
    data: { phase: 'instructions_2' }
  });

  timeline.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: function() {
      return `
        <div style="max-width:900px; margin:40px auto; font-family:Arial,sans-serif; color:black; text-align:left; line-height:1.7; font-size:22px;">
          <div style="text-align:center; font-size:30px; font-weight:700; margin-bottom:28px;">Оценка письменного задания</div>
          <p>${assignedFeedback.text}</p>
          <p style="margin-top:34px; text-align:center;"><strong>Нажмите пробел, чтобы продолжить.</strong></p>
        </div>`;
    },
    choices: [' '],
    data: {
      phase: 'feedback_message',
      feedback_condition: assignedFeedback.key,
      feedback_text: assignedFeedback.text
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
    type: jsPsychFullscreen,
    fullscreen_mode: false,
    delay_after: 0
  });

  timeline.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: instructionBlock(`
      <div style="text-align:center; font-size:28px; font-weight:700; margin-bottom:24px;">Основное задание завершено.</div>
      <p>Спасибо. Осталось ответить на несколько коротких вопросов о сообщении, которое вы увидели перед основной частью задания.</p>
      <p style="margin-top:28px; text-align:center;"><strong>Нажмите пробел, чтобы продолжить.</strong></p>
    `),
    choices: [' '],
    data: { phase: 'post_task_signpost' }
  });

  timeline.push({
    type: jsPsychSurveyHtmlForm,
    preamble: '<h3>Вопросы о сообщении</h3><p>Пожалуйста, оцените ваше впечатление от сообщения.</p>',
    html: `
      <div style="text-align:left; max-width:760px; margin:0 auto; line-height:1.8;">
        <p>1. Насколько вы согласны с данной оценкой?</p>
        ${[1,2,3,4,5,6,7].map(v => `<label style="margin-right:12px;"><input type="radio" name="agree_assessment" value="${v}" ${RESPONSES_REQUIRED ? 'required' : ''}> ${v}</label>`).join('')}
        <p style="margin-top:20px;">2. Насколько справедливым вам показалось это сообщение?</p>
        ${[1,2,3,4,5,6,7].map(v => `<label style="margin-right:12px;"><input type="radio" name="fairness_message" value="${v}" ${RESPONSES_REQUIRED ? 'required' : ''}> ${v}</label>`).join('')}
        <p style="margin-top:20px;">3. Насколько неприятным для вас было это сообщение?</p>
        ${[1,2,3,4,5,6,7].map(v => `<label style="margin-right:12px;"><input type="radio" name="message_unpleasant" value="${v}" ${RESPONSES_REQUIRED ? 'required' : ''}> ${v}</label>`).join('')}
        <p style="margin-top:8px; color:#555;">Шкала: 1 — совсем нет, 7 — очень сильно.</p>
      </div>
    `,
    button_label: 'Продолжить',
    data: { phase: 'message_questionnaire' }
  });

  timeline.push({
    type: jsPsychSurveyHtmlForm,
    preamble: '<h3>Дополнительные вопросы</h3><p>Ниже несколько вопросов о вашем впечатлении от исследования.</p>',
    html: `
      <div style="text-align:left; max-width:780px; margin:0 auto; line-height:1.8;">
        <p>1. Как вы думаете, какова была настоящая цель исследования?</p>
        <textarea name="study_guess" rows="4" style="width:100%;"></textarea>

        <p style="margin-top:18px;">2. Как вам кажется, использовались ли в исследовании какие-либо элементы, которые не были заранее полностью объяснены?</p>
        <select name="suspected_deception" style="width:100%; padding:8px;" ${SUSPICION_SELECT_REQUIRED ? 'required' : ''}>
          <option value="">Выберите вариант</option>
          <option value="yes">Да</option>
          <option value="maybe">Возможно</option>
          <option value="no">Нет</option>
        </select>

        <p style="margin-top:18px;">3. Если да или если у вас есть предположение, опишите, в чём именно это могло заключаться.</p>
        <textarea name="deception_guess" rows="4" style="width:100%;"></textarea>

        <p style="margin-top:18px;">4. Было ли что-то необычное или подозрительное в заданиях?</p>
        <textarea name="unusual_notes" rows="4" style="width:100%;"></textarea>

        <p style="margin-top:18px;">5. Дополнительный комментарий (необязательно).</p>
        <textarea name="final_comment" rows="4" style="width:100%;"></textarea>
      </div>
    `,
    button_label: 'Продолжить',
    data: { phase: 'suspicion_questionnaire' }
  });


  timeline.push({
    type: jsPsychCallFunction,
    async: true,
    func: function(done) {
      showSavingScreen();
      withTimeout(sendStage2DataToGoogleSheets(), 6000).then(function() {
        done();
      }).catch(function(err) {
        console.error(err);
        done();
      });
    },
    data: { phase: 'send_stage2_data' }
  });

  timeline.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: `
      <div style="max-width:900px; margin:40px auto; font-family:Arial,sans-serif; text-align:left; line-height:1.7; color:black;">
        <h2 style="text-align:center; margin-bottom:24px;">Спасибо за участие в нашем исследовании.</h2>

        <h3>Цель исследования</h3>
        <p>Цель данного исследования: изучить, как подростки принимают решения и как реагируют на различные формы социальной информации и обратной связи.</p>
        <p>Чтобы результаты исследования были достоверными, не вся информация о процедуре исследования сообщалась участникам заранее.</p>

        <h3>Оценочные сообщения</h3>
        <p>Во время выполнения задания некоторые участники могли получать сообщения с оценкой результата. Эти сообщения являлись частью экспериментальной процедуры и не отражали реальный уровень способностей или усилий участника.</p>
        <p>Такая процедура используется в психологических исследованиях для изучения того, как люди реагируют на различные виды обратной связи.</p>

        <h3>Ваши данные</h3>
        <p>Все данные, полученные в ходе исследования, будут обезличены. Результаты исследования могут быть использованы в научных публикациях только в обобщённом виде.</p>

        <h3>Контакт исследователя</h3>
        <p>Если у вас или у вашего родителя/законного представителя возникли вопросы о данном исследовании, вы можете связаться с исследователем.</p>
        <p><b>Контакт:</b><br>Тотурбиев Бадыр<br>badyrc@mail.ru</p>

        <p style="margin-top:28px; text-align:center;"><button id="finalFinishButton" style="padding:12px 22px; font-size:18px;">Завершить</button></p>
      </div>
    `,
    choices: "NO_KEYS",
    on_load: function() {
      document.getElementById('finalFinishButton').onclick = function() {
        try { window.close(); } catch (e) {}
        document.body.innerHTML = '';
      };
    },
    data: { phase: 'final_debrief' }
  });

  jsPsych.run(timeline);
})();
