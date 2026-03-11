const noteInput = document.getElementById("noteInput");
const summariseBtn = document.getElementById("summariseBtn");
const loadSampleBtn = document.getElementById("loadSampleBtn");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");

const summaryText = document.getElementById("summaryText");
const issuesList = document.getElementById("issuesList");
const actionsList = document.getElementById("actionsList");
const risksList = document.getElementById("risksList");
const followupList = document.getElementById("followupList");

// A few fake sample notes for quick testing from the browser.
const fakeSamples = [
  `Patient: Test Patient A (fictional)\nAge: 57\nPresenting complaint: 3 days dry cough and mild fever.\nHistory: Hypertension, on lisinopril.\nAssessment: likely viral upper respiratory infection. BP slightly elevated today.\nPlan: Continue hydration, monitor blood pressure daily, return if shortness of breath or chest pain. Follow-up in 1 week if symptoms persist.`,
  `Patient: Test Patient B (fictional)\nAge: 41\nComplaint: Intermittent lower back pain for 2 weeks after lifting boxes.\nExam: no neurological deficit, tenderness in lumbar muscles.\nPlan: Start ibuprofen as needed, refer to physiotherapy, advise gentle stretches.\nRisk notes: Seek urgent care if weakness, numbness, or bowel/bladder changes occur.`,
  `Patient: Test Patient C (fictional)\nAge: 68\nVisit reason: Diabetes review.\nFindings: HbA1c higher than target, missed two recent doses of metformin.\nActions: Reinforce medication adherence, prescribe glucose log sheet, schedule nurse educator referral.\nFollow-up: review in 4 weeks with home glucose readings.`
];

function listFromArray(target, items) {
  target.innerHTML = "";

  if (!items || items.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No details provided.";
    target.appendChild(li);
    return;
  }

  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    target.appendChild(li);
  });
}

async function summariseNote() {
  const noteText = noteInput.value.trim();
  if (!noteText) {
    statusEl.textContent = "Please paste a clinical note first.";
    return;
  }

  summariseBtn.disabled = true;
  statusEl.textContent = "Summarising...";

  try {
    const response = await fetch("/api/summarise", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ note_text: noteText })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Something went wrong.");
    }

    summaryText.textContent = data.summary || "";
    listFromArray(issuesList, data.key_issues || []);
    listFromArray(actionsList, data.actions || []);
    listFromArray(risksList, data.risks || []);
    listFromArray(followupList, data.suggested_follow_up || []);

    resultEl.classList.remove("hidden");
    statusEl.textContent = "Done.";
  } catch (error) {
    statusEl.textContent = `Error: ${error.message}`;
  } finally {
    summariseBtn.disabled = false;
  }
}

function loadFakeSample() {
  const random = Math.floor(Math.random() * fakeSamples.length);
  noteInput.value = fakeSamples[random];
  statusEl.textContent = "Loaded fake sample note.";
}

summariseBtn.addEventListener("click", summariseNote);
loadSampleBtn.addEventListener("click", loadFakeSample);
