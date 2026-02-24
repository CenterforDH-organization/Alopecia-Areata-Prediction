const config = window.APP_CONFIG || {};
const API_BASE_URL = (config.API_BASE_URL || "http://127.0.0.1:9999").replace(/\/+$/, "");

const state = {
  fields: [],
};

const dom = {
  apiUrl: document.getElementById("api-url"),
  form: document.getElementById("prediction-form"),
  fieldsGrid: document.getElementById("fields-grid"),
  formError: document.getElementById("form-error"),
  submitBtn: document.getElementById("submit-btn"),
  resultPanel: document.getElementById("result-panel"),
  currentLabel: document.getElementById("current-label"),
  currentProbability: document.getElementById("current-probability"),
  improvedCard: document.getElementById("improved-card"),
  improvedLabel: document.getElementById("improved-label"),
  improvedProbability: document.getElementById("improved-probability"),
  recommendationWrap: document.getElementById("recommendation-wrap"),
  recommendationList: document.getElementById("recommendation-list"),
  patientInfoBody: document.getElementById("patient-info-body"),
};

function setError(message) {
  dom.formError.textContent = message || "";
}

function setLoading(isLoading) {
  dom.submitBtn.disabled = isLoading;
  dom.submitBtn.textContent = isLoading ? "분석 중..." : "분석하기";
}

function createFieldElement(field) {
  const wrapper = document.createElement("div");
  wrapper.className = "field";

  const label = document.createElement("label");
  label.setAttribute("for", field.id);
  label.textContent = field.label;

  if (field.unit) {
    const unit = document.createElement("span");
    unit.className = "unit";
    unit.textContent = `(${field.unit})`;
    label.appendChild(unit);
  }

  wrapper.appendChild(label);

  let input;
  if (field.kind === "select") {
    input = document.createElement("select");
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "선택하세요";
    input.appendChild(placeholder);

    for (const option of field.options || []) {
      const opt = document.createElement("option");
      opt.value = option.value;
      opt.textContent = option.label;
      input.appendChild(opt);
    }
  } else {
    input = document.createElement("input");
    input.type = "number";
    input.step = "any";
    input.inputMode = "decimal";
    input.placeholder = `${field.label} 입력`;
  }

  input.id = field.id;
  input.name = field.id;
  input.required = true;
  wrapper.appendChild(input);

  if (field.description) {
    const desc = document.createElement("p");
    desc.className = "field-desc";
    desc.textContent = field.description;
    wrapper.appendChild(desc);
  }

  return wrapper;
}

function renderFields(fields) {
  dom.fieldsGrid.innerHTML = "";
  for (const field of fields) {
    dom.fieldsGrid.appendChild(createFieldElement(field));
  }
}

async function loadSchema() {
  const response = await fetch(`${API_BASE_URL}/api/schema/kr`);
  if (!response.ok) {
    throw new Error("스키마를 불러오지 못했습니다.");
  }
  const data = await response.json();
  if (!Array.isArray(data.fields) || data.fields.length === 0) {
    throw new Error("스키마 데이터가 비어 있습니다.");
  }
  state.fields = data.fields;
  renderFields(state.fields);
}

function collectPayload() {
  const payload = {};

  for (const field of state.fields) {
    const element = document.getElementById(field.id);
    if (!element) {
      throw new Error(`필드가 렌더링되지 않았습니다: ${field.id}`);
    }
    const value = String(element.value || "").trim();
    if (!value) {
      throw new Error(`'${field.label}' 항목을 입력해 주세요.`);
    }
    payload[field.id] = value;
  }

  return payload;
}

function formatProbability(value) {
  return `${Number(value).toFixed(2)}%`;
}

function renderPatientInfo(patientInfo) {
  dom.patientInfoBody.innerHTML = "";
  for (const item of patientInfo || []) {
    const row = document.createElement("tr");

    const tdLabel = document.createElement("td");
    tdLabel.textContent = item.label;
    row.appendChild(tdLabel);

    const tdValue = document.createElement("td");
    tdValue.textContent = item.value;
    row.appendChild(tdValue);

    dom.patientInfoBody.appendChild(row);
  }
}

function renderRecommendations(recommendations) {
  dom.recommendationList.innerHTML = "";

  if (!recommendations || recommendations.length === 0) {
    dom.recommendationWrap.classList.add("hidden");
    return;
  }

  for (const rec of recommendations) {
    const li = document.createElement("li");
    li.textContent = rec;
    dom.recommendationList.appendChild(li);
  }
  dom.recommendationWrap.classList.remove("hidden");
}

function renderResult(data) {
  dom.currentLabel.textContent = data.current.label;
  dom.currentProbability.textContent = `원형탈모 확률: ${formatProbability(
    data.current.probability_percent
  )} (기준: ${data.current.threshold_percent}%)`;

  if (data.improved) {
    dom.improvedLabel.textContent = data.improved.label;
    dom.improvedProbability.textContent = `개선 후 확률: ${formatProbability(
      data.improved.probability_percent
    )}`;
    dom.improvedCard.classList.remove("hidden");
  } else {
    dom.improvedCard.classList.add("hidden");
  }

  renderRecommendations(data.recommendations);
  renderPatientInfo(data.patient_info);
  dom.resultPanel.classList.remove("hidden");
  dom.resultPanel.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function handleSubmit(event) {
  event.preventDefault();
  setError("");

  let payload;
  try {
    payload = collectPayload();
  } catch (error) {
    setError(error.message);
    return;
  }

  try {
    setLoading(true);
    const response = await fetch(`${API_BASE_URL}/api/predict/kr`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "예측 요청에 실패했습니다.");
    }
    renderResult(data);
  } catch (error) {
    setError(error.message || "요청 중 오류가 발생했습니다.");
  } finally {
    setLoading(false);
  }
}

async function init() {
  dom.apiUrl.textContent = API_BASE_URL;
  dom.form.addEventListener("submit", handleSubmit);

  try {
    await loadSchema();
  } catch (error) {
    setError(
      `${error.message} API 주소와 백엔드 실행 상태를 확인하세요. (${API_BASE_URL})`
    );
  }
}

document.addEventListener("DOMContentLoaded", init);

