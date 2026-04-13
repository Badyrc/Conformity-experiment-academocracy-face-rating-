// CLEAN VERSION - LOCAL DOWNLOAD ONLY

const jsPsych = initJsPsych();

function downloadText(filename, text) {
  const blob = new Blob([text], { type: 'text/csv' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
}

function buildFormatted() {
  const data = jsPsych.data.get().values();
  const row = {};
  data.forEach((t, i) => {
    if (t.phase === 'main_rating') {
      row[`face_${i}_majority`] = t.majority_rating;
      row[`face_${i}_chosen`] = t.response;
    }
  });
  return row;
}

jsPsych.run([
  {
    type: jsPsychCallFunction,
    func: () => {
      const raw = jsPsych.data.get().csv();
      const formatted = JSON.stringify(buildFormatted());
      downloadText("stage2_raw.csv", raw);
      downloadText("stage2_formatted.csv", formatted);
    }
  }
]);
