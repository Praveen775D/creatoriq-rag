import IngestForm
from "@/components/IngestForm";

import ChatPanel
from "@/components/ChatPanel";

export default function Home() {

  return (
    <main className="container mx-auto p-6">

      <h1 className="text-3xl font-bold mb-6">
        CreatorIQ RAG Analyzer
      </h1>

      <IngestForm />

      <div className="mt-8">
        <ChatPanel />
      </div>

    </main>
  );
}