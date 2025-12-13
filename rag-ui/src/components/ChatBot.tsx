import { useState, useEffect } from "react";
import { MessageResponse } from "@/components/ai-elements/message";
import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from "@/components/ai-elements/conversation";
import {
  PromptInput,
  PromptInputTextarea,
  PromptInputActionMenu,
  PromptInputActionMenuTrigger,
  PromptInputActionMenuContent,
  PromptInputSubmit,
  PromptInputFooter,
  PromptInputTools,
} from "@/components/ai-elements/prompt-input";
import { Spinner } from "@/components/ui/spinner";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { User, Bot, Settings } from "lucide-react";
import { DropdownMenuItem } from "@/components/ui/dropdown-menu";

interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
}

export default function ChatBot() {
   const [messages, setMessages] = useState<Message[]>([]);
   const [isLoading, setIsLoading] = useState(false);
   const [models, setModels] = useState<string[]>([]);
   const [selectedModel, setSelectedModel] = useState("");

   useEffect(() => {
    const fetchModels = async () => {
      try {
        const response = await fetch("/api/models");
        const data = await response.json();
        setModels(data.data || []);
        if (data.data && data.data.length > 0) {
          setSelectedModel(data.data[0]);
        }
      } catch (error) {
        console.error("Failed to fetch models:", error);
      }
    };
    fetchModels();
  }, []);

  const handleSendMessage = async (message: { text: string; files: any[] }) => {
    const inputText = message.text.trim();
    if (!inputText) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputText,
      role: "user",
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    const updatedMessages = [...messages, userMessage];
    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      content: "",
      role: "assistant",
    };

    setMessages((prev) => [...prev, assistantMessage]);

    try {
      const response = await fetch("/api/chat?stream=true", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: selectedModel,
          messages: updatedMessages.map((m) => ({
            role: m.role,
            content: m.content,
          })),
        }),
      });

      if (!response.ok) throw new Error("API request failed");

      const reader = response.body?.getReader();
      if (!reader) throw new Error("No response stream");

      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
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
      console.error("Chat error:", error);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMessage.id
            ? {
                ...m,
                content: "Error: Failed to get response from the backend.",
              }
            : m,
        ),
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <div className="flex flex-col h-screen w-screen bg-gradient-to-br from-slate-50 via-white to-slate-50 overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200/50 bg-white/50">
          <h1 className="text-lg font-semibold text-slate-900">Example RAG App</h1>
          <p className="text-sm text-slate-600">A template for building RAG applications</p>
        </div>

        {/* Messages Container */}
        <Conversation className="px-6">
        <ConversationContent className="space-y-4 px-0 pr-4">
           {messages.map((message) => {
            // Skip empty assistant messages while loading
            if (
              message.role === "assistant" &&
              message.content === "" &&
              isLoading
            ) {
              return null;
            }

            return (
              <div
                key={message.id}
                className={`flex animate-in fade-in slide-in-from-bottom-3 gap-3 items-start ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {message.role === "assistant" && (
                  <Avatar className="size-9 flex-shrink-0 mt-1">
                    <AvatarFallback className="bg-gradient-to-br from-blue-100 to-cyan-100 text-blue-600">
                      <Bot className="size-5" />
                    </AvatarFallback>
                  </Avatar>
                )}
                <div
                  className={`${
                    message.role === "user"
                      ? "max-w-xs lg:max-w-md"
                      : "max-w-2xl lg:max-w-4xl"
                  }`}
                >
                  <div
                    className={`px-4 py-3 rounded-2xl transition-all ${
                      message.role === "user"
                        ? "bg-gradient-to-br from-blue-500 to-blue-600 text-white shadow-md hover:shadow-lg"
                        : "bg-gradient-to-br from-slate-100 to-slate-50 text-slate-900 border border-slate-200/60 shadow-sm"
                    }`}
                  >
                    {message.role === "assistant" ? (
                      <MessageResponse className="text-sm leading-relaxed [&>*:first-child]:mt-0 [&>*:last-child]:mb-0 [&_code]:bg-slate-200/50 [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:rounded [&_code]:text-slate-900">
                        {message.content}
                      </MessageResponse>
                    ) : (
                      <p className="text-sm leading-relaxed break-words">
                        {message.content}
                      </p>
                    )}
                  </div>
                </div>
                {message.role === "user" && (
                  <Avatar className="size-9 flex-shrink-0 mt-1">
                    <AvatarFallback className="bg-gradient-to-br from-slate-200 to-slate-300 text-slate-700">
                      <User className="size-5" />
                    </AvatarFallback>
                  </Avatar>
                )}
              </div>
            );
          })}
          {isLoading && (
            <div className="flex animate-in fade-in slide-in-from-bottom-3 gap-3 items-start">
              <Avatar className="size-9 flex-shrink-0 mt-1">
                <AvatarFallback className="bg-gradient-to-br from-blue-100 to-cyan-100 text-blue-600">
                  <Bot className="size-5" />
                </AvatarFallback>
              </Avatar>
              <div className="bg-gradient-to-br from-slate-100 to-slate-50 text-slate-600 px-4 py-3 rounded-2xl flex items-center gap-2 border border-slate-200/60 shadow-sm">
                <Spinner className="size-4 text-slate-500" />
                <span className="text-sm text-slate-500">Thinking...</span>
              </div>
            </div>
          )}
        </ConversationContent>
        <ConversationScrollButton />
      </Conversation>

      {/* Input Area */}
      <PromptInput
        onSubmit={handleSendMessage}
        className="px-6 py-4"
      >
        <PromptInputTextarea
          placeholder="Ask something..."
          className="bg-white text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-0 rounded-2xl"
        />
        <PromptInputFooter className="gap-3 bg-white">
          <PromptInputTools className="flex-1">
            <PromptInputActionMenu>
              <PromptInputActionMenuTrigger className="h-10 w-10 rounded-full border border-slate-200 text-slate-500 hover:text-slate-700 hover:bg-slate-100/50 transition-colors">
                <Settings className="size-4" />
              </PromptInputActionMenuTrigger>
              <PromptInputActionMenuContent align="end" className="w-48">
                <div className="px-2 py-1.5">
                  <p className="text-xs font-semibold text-slate-700 px-1">
                    Model
                  </p>
                </div>
                <div className="border-t border-slate-200/50"></div>
                {models.map((model) => (
                  <DropdownMenuItem
                    key={model}
                    onClick={() => setSelectedModel(model)}
                    className={`cursor-pointer transition-colors text-sm ${
                      selectedModel === model
                        ? "bg-blue-100/50 text-blue-700"
                        : "text-slate-700 hover:bg-slate-100"
                    }`}
                  >
                    {model}
                  </DropdownMenuItem>
                ))}
              </PromptInputActionMenuContent>
            </PromptInputActionMenu>
          </PromptInputTools>
          <PromptInputSubmit className="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 text-white hover:shadow-lg hover:to-blue-700 active:scale-95 disabled:opacity-50" />
        </PromptInputFooter>
      </PromptInput>
      </div>
    </>
  );
}
