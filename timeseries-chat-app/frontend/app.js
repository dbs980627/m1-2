const API = window.APP_CONFIG.API_BASE_URL;
const $ = (id) => document.getElementById(id);
let convId = null;
let history = [];

async function api(path, opts = {}) {
  const timer = setTimeout(() => ($("notice").hidden = false), 3000); // 콜드스타트 안내
  try {
    const res = await fetch(API + path, {
      headers: { "Content-Type": "application/json" },
      ...opts,
      body: opts.body ? JSON.stringify(opts.body) : undefined,
    });
    if (!res.ok) {
      const e = await res.json().catch(() => ({}));
      const d = e.detail;
      throw new Error(typeof d === "string" ? d : d ? "입력값을 확인해 주세요." : `오류 ${res.status}`);
    }
    return await res.json();
  } finally {
    clearTimeout(timer);
    $("notice").hidden = true;
  }
}

/* ---------- 요약 ---------- */
async function loadSummary() {
  try {
    const s = await api("/api/data/summary");
    if (!s.count) { $("summary").textContent = "데이터가 없습니다."; return; }
    const rows = [
      ["기간", `${s.start_date} ~ ${s.end_date}`], ["개수", s.count], ["평균", s.mean],
      ["최대", `${s.max.value} (${s.max.date})`], ["최소", `${s.min.value} (${s.min.date})`],
      ["최근값", s.latest.value], ["추세", `${s.trend} (${s.trend_change_pct}%)`],
    ];
    const dl = document.createElement("dl");
    rows.forEach(([k, v]) => {
      const dt = document.createElement("dt"); dt.textContent = k;
      const dd = document.createElement("dd"); dd.textContent = v;
      dl.append(dt, dd);
    });
    $("summary").replaceChildren(dl);
  } catch (e) { $("summary").textContent = "요약 불러오기 실패: " + e.message; }
}

/* ---------- 채팅 ---------- */
function addMsg(role, text) {
  const d = document.createElement("div");
  d.className = "msg " + role; d.textContent = text;
  $("messages").append(d); $("messages").scrollTop = $("messages").scrollHeight;
}
function renderMessages(msgs) { $("messages").replaceChildren(); msgs.forEach((m) => addMsg(m.role, m.content)); }

$("chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = $("chat-input").value.trim();
  if (!text) return;
  $("chat-input").value = "";
  addMsg("user", text);
  $("loading").hidden = false;
  try {
    const r = await api("/api/chat", { method: "POST", body: { message: text, conversation_id: convId, history } });
    addMsg("assistant", r.reply);
    history.push({ role: "user", content: text }, { role: "assistant", content: r.reply });
    convId = r.conversation_id;
    loadConversations();
  } catch (err) { addMsg("assistant", "⚠️ " + err.message); }
  finally { $("loading").hidden = true; }
});

/* ---------- 대화 기록 ---------- */
$("new-chat").onclick = () => { convId = null; history = []; $("messages").replaceChildren(); loadConversations(); };

async function loadConversations() {
  try {
    const list = await api("/api/conversations");
    $("conv-list").replaceChildren(...list.map((c) => {
      const li = document.createElement("li");
      if (c.id === convId) li.className = "active";
      const t = document.createElement("span"); t.textContent = c.title || "(제목 없음)";
      const del = document.createElement("button"); del.textContent = "삭제"; del.className = "danger";
      del.onclick = async (ev) => {
        ev.stopPropagation();
        if (!confirm("이 대화를 삭제할까요?")) return;
        await api("/api/conversations/" + c.id, { method: "DELETE" });
        if (convId === c.id) $("new-chat").click(); else loadConversations();
      };
      li.onclick = async () => {
        const full = await api("/api/conversations/" + c.id);
        convId = full.id; history = full.messages; renderMessages(history); loadConversations();
      };
      li.append(t, del);
      return li;
    }));
  } catch (e) { console.error(e); }
}

/* ---------- 데이터 CRUD ---------- */
function status(msg, ok = true) { $("data-status").textContent = msg; $("data-status").className = "status " + (ok ? "ok" : "err"); }

function resetForm() {
  $("data-form").reset(); $("data-id").value = "";
  $("data-submit").textContent = "추가"; $("data-cancel").hidden = true;
}
$("data-cancel").onclick = resetForm;

$("data-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const body = { date: $("data-date").value, value: parseFloat($("data-value").value), memo: $("data-memo").value };
  const id = $("data-id").value;
  try {
    await api(id ? "/api/data/" + id : "/api/data", { method: id ? "PUT" : "POST", body });
    status(id ? "수정되었습니다." : "추가되었습니다.");
    resetForm(); loadData(); loadSummary();
  } catch (err) { status("저장 실패: " + err.message, false); }
});

async function loadData() {
  try {
    const rows = (await api("/api/data")).reverse(); // 최신순
    $("data-body").replaceChildren(...rows.map((r) => {
      const tr = document.createElement("tr");
      [r.date, r.value, r.memo].forEach((v) => { const td = document.createElement("td"); td.textContent = v; tr.append(td); });
      const td = document.createElement("td");
      const ed = document.createElement("button"); ed.textContent = "수정"; ed.className = "sub";
      ed.onclick = () => {
        $("data-id").value = r.id; $("data-date").value = r.date; $("data-value").value = r.value; $("data-memo").value = r.memo;
        $("data-submit").textContent = "저장"; $("data-cancel").hidden = false; window.scrollTo(0, document.body.scrollHeight);
      };
      const del = document.createElement("button"); del.textContent = "삭제"; del.className = "danger";
      del.onclick = async () => {
        if (!confirm("삭제할까요?")) return;
        try { await api("/api/data/" + r.id, { method: "DELETE" }); status("삭제되었습니다."); loadData(); loadSummary(); }
        catch (err) { status("삭제 실패: " + err.message, false); }
      };
      td.append(ed, " ", del); tr.append(td);
      return tr;
    }));
  } catch (e) { status("목록 불러오기 실패: " + e.message, false); }
}

loadSummary(); loadData(); loadConversations();
