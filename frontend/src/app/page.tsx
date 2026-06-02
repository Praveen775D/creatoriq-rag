import IngestForm from "../components/IngestForm";
import ChatPanel from "../components/ChatPanel";

export default function Home() {
  return (
    <main className="max-w-5xl mx-auto p-6">
      <header className="mb-8">
        <h1 className="text-3xl font-bold">
          CreatorIQ RAG Analyzer
        </h1>

        <p className="text-gray-600 mt-2">
          Compare YouTube & Instagram content using AI-powered RAG analysis
        </p>
      </header>

      {/* INGEST SECTION */}
      <section className="mb-10">
        <IngestForm />
      </section>

      {/* CHAT SECTION */}
      <section>
        <ChatPanel />
      </section>
    </main>
  );
}