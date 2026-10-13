import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";
const API_TIMEOUT = 15000;
const CHAT_TIMEOUT = 180000; // 3 minutes for AI responses

function getErrorMessage(error) {
  if (error?.name === "AbortError") {
    return "The request timed out. Check the backend terminal and try again.";
  }

  if (error instanceof Error) {
    return error.message;
  }

  if (typeof error === "string") {
    return error;
  }

  try {
    return JSON.stringify(error) || "Unknown error";
  } catch {
    return String(error);
  }
}

function App() {
  const [studentId, setStudentId] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [student, setStudent] = useState(null);
  const [insights, setInsights] = useState(null);
  const [studentLoading, setStudentLoading] = useState(false);
  const [notice, setNotice] = useState("");

  async function fetchJSON(url, options = {}, timeout = API_TIMEOUT) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        const detail = data?.detail;

        const message =
          typeof detail === "string"
            ? detail
            : detail != null
              ? JSON.stringify(detail)
              : `Request failed (${response.status})`;

        throw new Error(message);
      }

      return data;
    } finally {
      clearTimeout(timer);
    }
  }

  async function loadStudentData() {
    const id = studentId.trim();

    if (!/^\d+$/.test(id)) {
      setNotice("Enter a valid numeric Student ID.");
      return;
    }

    setStudentLoading(true);
    setNotice("");
    setStudent(null);
    setInsights(null);
    setMessages([]);

    try {
      const [studentResult, insightResult] = await Promise.allSettled([
        fetchJSON(`${API_URL}/student/${id}`),
        fetchJSON(`${API_URL}/student/${id}/insights`),
      ]);

      if (studentResult.status === "rejected") {
        throw studentResult.reason;
      }

      setStudent(studentResult.value);

      if (insightResult.status === "fulfilled") {
        const result = insightResult.value;
        setInsights(result.insights ?? result);
      } else {
        setInsights(null);
        setNotice(
          `Student loaded, but insights could not be loaded: ${getErrorMessage(
            insightResult.reason
          )}`
        );
      }
    } catch (error) {
      setStudent(null);
      setInsights(null);
      setNotice(
        error?.name === "AbortError"
          ? "Loading student data timed out. Check that the backend is running."
          : getErrorMessage(error)
      );
    } finally {
      setStudentLoading(false);
    }
  }

  async function askAI(customQuestion = null) {
    const finalQuestion = (customQuestion ?? question).trim();

    if (!finalQuestion || loading) return;

    if (!student) {
      setNotice("Load a valid student profile before chatting.");
      return;
    }

    const id = Number(studentId.trim());

    if (!Number.isInteger(id) || id <= 0) {
      setNotice("Invalid Student ID. Please reload the student profile.");
      return;
    }

    setMessages((previous) => [
      ...previous,
      { type: "user", text: finalQuestion },
    ]);

    setQuestion("");
    setNotice("");
    setLoading(true);

    try {
      const data = await fetchJSON(
        `${API_URL}/chat`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            student_id: id,
            question: finalQuestion,
          }),
        },
        CHAT_TIMEOUT
      );

      const rawAnswer =
        data.answer ??
        data.ai_response ??
        data.response ??
        data.message ??
        "The server returned no answer.";

      const answer =
        typeof rawAnswer === "string"
          ? rawAnswer
          : JSON.stringify(rawAnswer);

      setMessages((previous) => [
        ...previous,
        { type: "ai", text: answer },
      ]);

      // Refresh dashboard data independently.
      fetchJSON(`${API_URL}/student/${id}`)
        .then(setStudent)
        .catch((error) => {
          console.error("Student refresh:", error);
        });

      // Refresh insights without clearing existing insights on failure.
      fetchJSON(`${API_URL}/student/${id}/insights`)
        .then((result) => {
          setInsights(result.insights ?? result);
        })
        .catch((error) => {
          console.error("Insights refresh:", error);
          // Keep the previously loaded insights visible.
        });
    } catch (error) {
      console.error("EduAssist chat request failed:", error);

      const message =
        error?.name === "AbortError"
          ? "The AI response took longer than 3 minutes. Check the backend terminal and Ollama status."
          : getErrorMessage(error);

      setMessages((previous) => [
        ...previous,
        {
          type: "ai",
          text: `Unable to get a response: ${message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    askAI();
  }

  const quickQuestions = [
    "What is my current performance?",
    "What are my weak areas?",
    "Am I improving?",
    "How can I improve my performance?",
    "Give me an overall analysis",
    "Create a study plan for me",
  ];

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">EA</div>
          <div>
            <h1>EduAssist AI</h1>
            <p>Your Personal AI Academic Assistant</p>
          </div>
        </div>

        <div className="student-box">
          <label htmlFor="student-id">Student ID</label>
          <input
            id="student-id"
            value={studentId}
            onChange={(event) => setStudentId(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") loadStudentData();
            }}
            placeholder="Enter student ID"
            inputMode="numeric"
          />
          <button
            type="button"
            onClick={loadStudentData}
            disabled={studentLoading}
          >
            {studentLoading ? "Loading..." : "Load Student"}
          </button>
        </div>

        {notice && <p className="notice">{notice}</p>}

        <div className="sidebar-section">
          <p className="section-title">Quick Actions</p>
          {quickQuestions.map((item) => (
            <button
              className="quick-btn"
              key={item}
              onClick={() => askAI(item)}
              disabled={!student || loading}
            >
              {item}
            </button>
          ))}
        </div>

        <div className="pipeline">
          <p className="section-title">AI Pipeline</p>
          <div>✓ Student Intelligence</div>
          <div>✓ NLP Intent Engine</div>
          <div>✓ Academic Insights</div>
          <div>✓ Chat Response Engine</div>
        </div>
      </aside>

      <main className="main">
        <header className="header">
          <div>
            <p className="eyebrow">ACADEMIC INTELLIGENCE PLATFORM</p>
            <h2>
              Welcome to <span>EduAssist AI</span>
            </h2>
            <p className="subtitle">
              Analyze your performance, understand your weaknesses, and get
              personalized academic guidance.
            </p>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            API Connected
          </div>
        </header>

        <section className="analytics">
          <div className="metric-card">
            <p>Average Score</p>
            <h3>
              {student?.average_score ?? "--"}
              <small>%</small>
            </h3>
            <span>Current performance</span>
          </div>

          <div className="metric-card">
            <p>Performance</p>
            <h3 className="excellent">
              {student?.performance_category ?? "--"}
            </h3>
            <span>Academic category</span>
          </div>

          <div className="metric-card">
            <p>Assessments</p>
            <h3>{student?.assessment_count ?? "--"}</h3>
            <span>Recorded assessments</span>
          </div>

          <div className="metric-card">
            <p>Risk Level</p>
            <h3>
              {student?.risk_level ??
                insights?.priority?.priority ??
                "--"}
            </h3>
            <span>Academic focus</span>
          </div>
        </section>

        <section className="content-grid">
          <div className="chat-panel">
            <div className="panel-header">
              <div>
                <h3>Ask EduAssist AI</h3>
                <p>Ask questions about your performance or academics.</p>
              </div>
              <div className="ai-badge">Academic Chatbot</div>
            </div>

            <div className="messages">
              {!student && messages.length === 0 && (
                <div className="empty-chat">
                  <div className="empty-icon">✦</div>
                  <h3>Load your student profile first</h3>
                  <p>
                    Enter a valid Student ID to view performance and start
                    chatting.
                  </p>
                </div>
              )}

              {student && messages.length === 0 && (
                <div className="empty-chat">
                  <div className="empty-icon">✦</div>
                  <h3>How can I help you today?</h3>
                  <p>
                    Ask about your scores, weak areas, progress, risk, or study
                    plan.
                  </p>
                </div>
              )}

              {messages.map((message, index) => (
                <div
                  className={`message ${message.type}`}
                  key={`${index}-${message.type}`}
                >
                  <div className="message-label">
                    {message.type === "user" ? "You" : "EduAssist AI"}
                  </div>
                  <div className="message-text">{message.text}</div>
                </div>
              ))}

              {loading && (
                <div className="message ai">
                  <div className="message-label">EduAssist AI</div>
                  <div className="typing">
                    Analyzing your academic data and generating a response...
                  </div>
                </div>
              )}
            </div>

            <form className="chat-input" onSubmit={handleSubmit}>
              <input
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder={
                  student ? "Ask EduAssist AI..." : "Load a student first..."
                }
                disabled={!student || loading}
              />
              <button type="submit" disabled={!student || loading}>
                {loading ? "Wait..." : "Send"}
              </button>
            </form>
          </div>

          <div className="insights-panel">
            <div className="panel-header">
              <div>
                <h3>Academic Insights</h3>
                <p>Personalized intelligence</p>
              </div>
            </div>

            {!student ? (
              <div className="no-data">
                Load a valid student to view academic insights.
              </div>
            ) : !insights ? (
              <div className="no-data">
                Student loaded, but academic insights are unavailable.
              </div>
            ) : (
              <div className="insight-list">
                {[
                  [
                    "Performance",
                    insights.performance_insight || insights.summary,
                  ],
                  ["Consistency", insights.consistency_insight],
                  ["Trend", insights.trend_insight],
                  ["Weak Areas", insights.weakness_insight],
                  ["Engagement", insights.engagement_insight],
                ]
                  .filter((item) => item[1])
                  .map(([title, description]) => (
                    <div className="insight-item" key={title}>
                      <span>{title}</span>
                      <p>{description}</p>
                    </div>
                  ))}

                {insights.priority && (
                  <div className="priority-box">
                    <strong>
                      Priority:{" "}
                      {typeof insights.priority === "object"
                        ? insights.priority.priority
                        : insights.priority}
                    </strong>

                    {typeof insights.priority === "object" &&
                      insights.priority.reasons?.length > 0 && (
                        <p>{insights.priority.reasons.join(", ")}</p>
                      )}
                  </div>
                )}

                {insights.recommendations?.length > 0 && (
                  <div className="insight-item">
                    <span>Recommendations</span>
                    {insights.recommendations.map((item, index) => (
                      <p key={index}>• {item}</p>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;