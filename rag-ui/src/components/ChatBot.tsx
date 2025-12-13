import { useState, useRef, useEffect } from 'react';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
}

export default function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [models, setModels] = useState<string[]>([]);
  const [selectedModel, setSelectedModel] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const response = await fetch('/api/models');
        const data = await response.json();
        setModels(data.data || []);
        if (data.data && data.data.length > 0) {
          setSelectedModel(data.data[0]);
        }
      } catch (error) {
        console.error('Failed to fetch models:', error);
      }
    };
    fetchModels();
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    const updatedMessages = [...messages, userMessage];
    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      content: '',
      role: 'assistant',
    };

    setMessages((prev) => [...prev, assistantMessage]);

    try {
      const response = await fetch('/api/chat?stream=true', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: selectedModel,
          messages: updatedMessages.map((m) => ({
            role: m.role,
            content: m.content,
          })),
        }),
      });

      if (!response.ok) throw new Error('API request failed');

      const reader = response.body?.getReader();
      if (!reader) throw new Error('No response stream');

      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const jsonStr = line.slice(6);
            if (jsonStr) {
              const data = JSON.parse(jsonStr);
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantMessage.id
                    ? { ...m, content: m.content + data }
                    : m,
                ),
              );
            }
          }
        }
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMessage.id
            ? {
                ...m,
                content:
                  'Error: Failed to get response from the backend.',
              }
            : m,
        ),
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto bg-card border border-border rounded-lg shadow-lg overflow-hidden">
      <div className="bg-primary text-primary-foreground px-6 py-4 border-b border-border space-y-3">
        <h1 className="text-2xl font-semibold">RAG Chatbot</h1>
        <div className="flex gap-2">
          <label htmlFor="model-select" className="text-sm font-medium">
            Model:
          </label>
          <select
            id="model-select"
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            disabled={isLoading}
            className="flex-1 px-3 py-1 rounded bg-primary-foreground text-primary text-sm focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50"
          >
            {models.map((model) => (
              <option key={model} value={model}>
                {model}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-3 scroll-smooth">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex animate-in fade-in slide-in-from-bottom-2 ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.role === 'user'
                  ? 'bg-primary text-primary-foreground rounded-br-none'
                  : 'bg-muted text-foreground rounded-bl-none'
              }`}
            >
              <p className="text-sm leading-relaxed break-words">{message.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start animate-in fade-in slide-in-from-bottom-2">
            <div className="bg-muted text-foreground px-4 py-2 rounded-lg rounded-bl-none">
              <p className="text-sm animate-pulse">Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form
        onSubmit={handleSendMessage}
        className="flex gap-2 px-6 py-4 bg-card border-t border-border"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
          className="flex-1 px-4 py-2 rounded-full bg-input border border-border text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="px-6 py-2 bg-primary text-primary-foreground rounded-full font-medium hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
        >
          Send
        </button>
      </form>
    </div>
  );
}
