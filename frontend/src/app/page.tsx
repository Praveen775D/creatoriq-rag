import IngestForm from "../components/IngestForm";
import ChatPanel from "../components/ChatPanel";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#030712] text-white overflow-hidden">

      {/* Background */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute top-0 left-0 h-[500px] w-[500px] rounded-full bg-violet-600/20 blur-[180px]" />
        <div className="absolute bottom-0 right-0 h-[500px] w-[500px] rounded-full bg-cyan-500/20 blur-[180px]" />
        <div className="absolute top-1/2 left-1/2 h-[400px] w-[400px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-pink-500/10 blur-[180px]" />
      </div>

      <div className="max-w-7xl mx-auto px-6 py-10">

        {/* NAVBAR */}
        <nav className="flex items-center justify-between mb-12">

          <div>
            <h1 className="text-3xl font-black bg-gradient-to-r from-cyan-400 via-violet-400 to-pink-500 bg-clip-text text-transparent">
              CreatorIQ
            </h1>

            <p className="text-slate-400 text-sm">
              AI Creator Intelligence Platform
            </p>
          </div>

          <div className="hidden md:flex items-center gap-4">
            <span className="px-4 py-2 rounded-full border border-white/10 bg-white/5 text-sm">
              LangChain
            </span>

            <span className="px-4 py-2 rounded-full border border-white/10 bg-white/5 text-sm">
              ChromaDB
            </span>

            <span className="px-4 py-2 rounded-full border border-white/10 bg-white/5 text-sm">
              GPT-4o
            </span>
          </div>

        </nav>

        {/* HERO */}
        <section className="text-center mb-14">

          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-violet-500/20 bg-violet-500/10 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            AI Powered Video Intelligence
          </div>

          <h2 className="text-6xl md:text-7xl font-black leading-tight mb-6">
            Compare Social Videos
            <br />
            <span className="bg-gradient-to-r from-cyan-400 via-violet-400 to-pink-500 bg-clip-text text-transparent">
              Using RAG + AI
            </span>
          </h2>

          <p className="max-w-3xl mx-auto text-slate-400 text-lg">
            Analyze YouTube Shorts and Instagram Reels using
            transcript intelligence, vector search, engagement
            analytics and AI-powered recommendations.
          </p>

        </section>

        {/* INPUT PANEL */}
        <section className="mb-12">

          <div className="rounded-[32px] border border-white/10 bg-white/[0.03] backdrop-blur-2xl p-8 shadow-[0_0_60px_rgba(0,0,0,0.4)]">

            <div className="flex items-center gap-3 mb-6">
              <div className="h-10 w-10 rounded-2xl bg-gradient-to-r from-cyan-500 to-violet-500 flex items-center justify-center">
                ⚡
              </div>

              <div>
                <h3 className="text-xl font-bold">
                  Video Intelligence Engine
                </h3>

                <p className="text-slate-400 text-sm">
                  Analyze two videos and build a RAG knowledge base
                </p>
              </div>
            </div>

            <IngestForm />

          </div>

        </section>

        {/* FEATURES */}
        <section className="grid md:grid-cols-4 gap-6 mb-12">

          {[
            {
              title: "Transcript Analysis",
              icon: "📝",
              desc: "Extract & compare spoken content",
            },
            {
              title: "Vector Search",
              icon: "🔍",
              desc: "Semantic retrieval using embeddings",
            },
            {
              title: "Engagement Insights",
              icon: "📈",
              desc: "Performance & growth analytics",
            },
            {
              title: "AI Recommendations",
              icon: "🤖",
              desc: "Improve content strategy instantly",
            },
          ].map((card) => (
            <div
              key={card.title}
              className="
                rounded-3xl
                border border-white/10
                bg-white/[0.03]
                p-6
                hover:border-violet-500/40
                hover:-translate-y-1
                transition-all
              "
            >
              <div className="text-3xl mb-4">
                {card.icon}
              </div>

              <h3 className="font-bold text-lg mb-2">
                {card.title}
              </h3>

              <p className="text-slate-400 text-sm">
                {card.desc}
              </p>
            </div>
          ))}

        </section>

        {/* AI CHAT */}
        <section>

          <div className="rounded-[32px] border border-white/10 bg-white/[0.03] backdrop-blur-2xl overflow-hidden">

            <div className="border-b border-white/10 p-6">

              <div className="flex items-center gap-4">

                <div className="h-12 w-12 rounded-2xl bg-gradient-to-r from-pink-500 to-violet-500 flex items-center justify-center text-xl">
                  
                </div>

                <div>
                  <h3 className="text-2xl font-bold">
                    CreatorIQ Assistant
                  </h3>

                  <p className="text-slate-400">
                    RAG-powered creator intelligence
                  </p>
                </div>

              </div>

            </div>

            <div className="p-8">
              <ChatPanel />
            </div>

          </div>

        </section>

      </div>
    </main>
  );
}