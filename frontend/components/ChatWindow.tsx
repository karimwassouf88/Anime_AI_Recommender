"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => crypto.randomUUID());
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage() {
    if (!input.trim() || loading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: input,
          session_id: sessionId,
        }),
      });

      const data = await res.json();
      const assistantMessage: Message = {
        role: "assistant",
        content: data.reply,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        role: "assistant",
        content: "Something went wrong. Please try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        maxWidth: "800px",
        margin: "0 auto",
        borderLeft: "1px solid var(--border)",
        borderRight: "1px solid var(--border)",
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: "24px 32px",
          borderBottom: "1px solid var(--border)",
          display: "flex",
          alignItems: "center",
          gap: "16px",
          background: "var(--bg-secondary)",
        }}
      >
        <div>
          <h1
            style={{
              fontFamily: "var(--font-display)",
              fontSize: "18px",
              fontWeight: "700",
              letterSpacing: "0.05em",
              color: "var(--text-primary)",
            }}
          >
            雅
          </h1>
          <p
            style={{
              fontSize: "14px",
              color: "var(--accent-red)",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              marginTop: "2px",
            }}
          >
            Miyabi AI
          </p>
        </div>
      </div>

      {/* Messages */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "32px",
          display: "flex",
          flexDirection: "column",
          gap: "24px",
        }}
      >
        {messages.length === 0 && (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
              gap: "16px",
              opacity: 0.4,
            }}
          >
            <div
              style={{
                fontFamily: "var(--font-display)",
                fontSize: "48px",
                color: "var(--accent-red)",
              }}
            >
              神
            </div>
            <p
              style={{
                fontSize: "11px",
                letterSpacing: "0.2em",
                textTransform: "uppercase",
                color: "var(--text-secondary)",
              }}
            >
              tell me what kind of masterpeice are u looking for
            </p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: msg.role === "user" ? "flex-end" : "flex-start",
              gap: "6px",
            }}
          >
            <span
              style={{
                fontSize: "9px",
                letterSpacing: "0.2em",
                textTransform: "uppercase",
                color: "var(--text-dim)",
              }}
            >
              {msg.role === "user" ? "you" : "oracle"}
            </span>
            <div
              style={{
                maxWidth: "80%",
                padding: "14px 18px",
                borderRadius:
                  msg.role === "user"
                    ? "12px 12px 2px 12px"
                    : "12px 12px 12px 2px",
                background:
                  msg.role === "user"
                    ? "var(--accent-red-dim)"
                    : "var(--bg-elevated)",
                border: `1px solid ${msg.role === "user" ? "var(--accent-red)" : "var(--border-accent)"}`,
                fontSize: "13px",
                lineHeight: "1.7",
                color: "var(--text-primary)",
                whiteSpace: "pre-wrap",
              }}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "flex-start",
              gap: "6px",
            }}
          >
            <span
              style={{
                fontSize: "9px",
                letterSpacing: "0.2em",
                textTransform: "uppercase",
                color: "var(--text-dim)",
              }}
            >
              Miyabi
            </span>
            <div
              style={{
                padding: "14px 18px",
                borderRadius: "12px 12px 12px 2px",
                background: "var(--bg-elevated)",
                border: "1px solid var(--border-accent)",
                display: "flex",
                gap: "6px",
                alignItems: "center",
              }}
            >
              {[0, 1, 2].map((i) => (
                <div
                  key={i}
                  style={{
                    width: "6px",
                    height: "6px",
                    borderRadius: "50%",
                    background: "var(--accent-red)",
                    animation: "pulse 1.2s ease-in-out infinite",
                    animationDelay: `${i * 0.2}s`,
                  }}
                />
              ))}
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div
        style={{
          padding: "24px 32px",
          borderTop: "1px solid var(--border)",
          background: "var(--bg-secondary)",
          display: "flex",
          gap: "12px",
          alignItems: "flex-end",
        }}
      >
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe what you want to watch or feel while watching ..."
          rows={1}
          style={{
            flex: 1,
            background: "var(--bg-input)",
            border: "1px solid var(--border)",
            borderRadius: "50px",
            padding: "10px 14px",
            color: "var(--text-primary)",
            fontFamily: "var(--font-mono)",
            fontSize: "13px",
            resize: "none",
            outline: "none",
            lineHeight: "1.6",
            transition: "border-color 0.2s",
          }}
          onFocus={(e) =>
            (e.target.style.borderColor = "var(--accent-red-dim)")
          }
          onBlur={(e) => (e.target.style.borderColor = "var(--border)")}
        />
        <button
          onClick={sendMessage}
          disabled={loading || !input.trim()}
          style={{
            background:
              loading || !input.trim()
                ? "var(--bg-elevated)"
                : "var(--accent-red)",
            border: "1px solid var(--border-accent)",
            borderRadius: "50px",
            padding: "12px 20px",
            color:
              loading || !input.trim()
                ? "var(--text-dim)"
                : "var(--text-primary)",
            fontFamily: "var(--font-mono)",
            fontSize: "12px",
            letterSpacing: "0.1em",
            cursor: loading || !input.trim() ? "not-allowed" : "pointer",
            transition: "all 0.2s",
            whiteSpace: "nowrap",
          }}
        >
          {loading ? "..." : "送信"}
        </button>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.3; transform: scale(0.8); }
          50% { opacity: 1; transform: scale(1); }
        }
      `}</style>
    </div>
  );
}
