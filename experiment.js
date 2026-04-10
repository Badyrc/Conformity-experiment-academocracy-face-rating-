(async function() {
  const jsPsych = initJsPsych({
    show_progress_bar: false,
    auto_update_progress_bar: false,
    on_finish: function() {
      const pid = jsPsych.data.get().filter({trial_type: 'survey-html-form'}).last(1).values()[0]?.response?.participant_id || '001';
      const stamp = new Date().toISOString().replace(/[:.]/g, '-');
      const csv = jsPsych.data.get().csv();
      downloadText(`${pid}_attractive_${stamp}.csv`, csv, 'text/csv');

      document.body.innerHTML = `
        <div class="jspsych-content" style="max-width:900px; margin:60px auto; font-family:Arial,sans-serif; text-align:center;">
          <h2>Experiment finished</h2>
          <p>Your data file has been downloaded to this device.</p>
          <p><strong>Important:</strong> GitHub Pages does not save data to the repository by itself, because it is static hosting.</p>
        </div>`;
    }
  });

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
        <div class="response-hint">Press a number from <strong>1</strong> to <strong>9</strong>.</div>
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
        <p>Put <code>index.html</code>, <code>experiment.js</code>, <code>practicepics.xlsx</code>, <code>pics.xlsx</code>, and your image files in the same folder.</p>
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
    type: jsPsychSurveyHtmlForm,
    preamble: '<h3>Participant information</h3>',
    html: `
      <p><label>Пол (1-М, 2-Ж): <input name="sex" required></label></p>
      <p><label>Возраст: <input name="age" required></label></p>
      <p><label>Номер участника: <input name="participant_id" value="001" required></label></p>
    `,
    button_label: 'Continue'
  });

  timeline.push({
    type: jsPsychFullscreen,
    fullscreen_mode: true,
    message: '<p>The experiment will switch to full-screen mode.</p>',
    button_label: 'Start'
  });

  timeline.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: `
      <div style="max-width:1000px; margin:0 auto; font-family:Arial,sans-serif; color:black; text-align:left; line-height:1.55; font-size:24px;">
        Добро пожаловать в эксперимент!<br><br>
        В этом эксперименте вам нужно будет оценивать привлекательность лиц.<br><br>
        Сначала в центре экрана появится лицо.<br><br>
        После того как лицо исчезнет, в центре экрана будет показана оценка других участников.<br><br>
        Зелёное число показывает, какую оценку поставило большинство других участников, а процент показывает долю участников, поставивших эту оценку.<br><br>
        Вам нужно оценить лицо по шкале от 1 (очень непривлекательно) до 9 (очень привлекательно).<br><br>
        Пожалуйста, старайтесь давать оценку как можно быстрее, не раздумывая слишком долго.<br><br>
        Во время эксперимента постарайтесь держать взгляд направленным в центр экрана.<br><br>
        Сначала мы проведём короткую тренировочную серию, чтобы показать, как будет проходить эксперимент.<br><br>
        Если вы готовы, нажмите пробел, чтобы начать.
      </div>
    `,
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
    stimulus: `
      <div style="max-width:1000px; margin:0 auto; font-family:Arial,sans-serif; color:black; text-align:left; line-height:1.55; font-size:28px;">
        The practice section has concluded.<br><br>
        If you are still unclear about what you have to do, please inform the experimenter.<br><br>
        If everything is clear, please read the following:<br><br>
        The work you have completed 5 minutes ago has been graded by the Academocracy AI.<br><br>
        It will give you its personal and honest opinion on the work you have completed.<br><br>
        You do not have to do anything with the feedback other than read it.<br><br>
        After reading it, continue onto the rest of the experiment.<br><br>
        If everything is clear, and you are ready to read the feedback, please press SPACEBAR.
      </div>
    `,
    choices: [' '],
    data: { phase: 'instructions_2' }
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

  jsPsych.run(timeline);
})();
