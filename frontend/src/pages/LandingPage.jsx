import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ArrowRight, BarChart3, Check, ChevronDown, Menu, Sparkles, Target, X, Zap } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

const features = [
  { icon: Target, title: 'Know who needs attention', text: 'Rank prospects with explainable scoring instead of relying on a generic lead list.' },
  { icon: Sparkles, title: 'Understand why now', text: 'Turn stored growth, hiring and leadership signals into a clear reason to contact.' },
  { icon: Zap, title: 'Go from insight to action', text: 'Generate reviewed outreach, build a sequence and move the lead into a measurable campaign.' },
  { icon: BarChart3, title: 'See what happened', text: 'Follow sends, replies, interested leads and meetings from one focused workspace.' },
]

const workflow = [
  ['01', 'Lead', 'Bring your prospect list into one focused workspace.'],
  ['02', 'Signal', 'Capture the business trigger attached to the prospect.'],
  ['03', 'Reason', 'See a transparent score and the Why Now explanation.'],
  ['04', 'Message', 'Create a role-aware outreach draft and edit it.'],
  ['05', 'Sequence', 'Use Day 1, Day 3 and Day 6 follow-ups.'],
  ['06', 'Result', 'Track activity, replies and meetings.'],
]

const faqs = [
  ['Does SignalFlow AI replace my CRM?', 'No. The MVP is a focused sales-execution layer for prioritization, outreach and follow-up.'],
  ['Can I review the AI message before it is sent?', 'Yes. Generated copy remains editable and user-controlled.'],
  ['Can I send real emails?', 'Yes. The latest version can send through a Gmail SMTP account configured with a Google App Password.'],
  ['Can I use the app without an AI API key?', 'Yes. A deterministic fallback can still generate a draft.'],
]

export default function LandingPage() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [mobileOpen, setMobileOpen] = useState(false)
  const [openFaq, setOpenFaq] = useState(0)

  const goLogin = () => navigate(user ? '/dashboard' : '/login')
  const goRegister = () => navigate(user ? '/dashboard' : '/register')

  return (
    <div className="min-h-screen overflow-x-hidden bg-[#f8fafc] text-slate-900">
      <div className="pointer-events-none fixed inset-0 -z-10 bg-[radial-gradient(circle_at_15%_15%,rgba(99,102,241,.16),transparent_28%),radial-gradient(circle_at_85%_20%,rgba(14,165,233,.12),transparent_26%),linear-gradient(to_bottom,#f8fafc,#eef2ff_46%,#f8fafc)]" />
      <header className="fixed inset-x-0 top-0 z-50 border-b border-white/60 bg-white/80 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-5 lg:px-8">
          <button onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} className="flex items-center gap-2 font-black tracking-tight">
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-950 text-white shadow-lg shadow-indigo-200"><Zap size={17} className="text-indigo-300" /></span>
            <span>SignalFlow<span className="text-indigo-600"> AI</span></span>
          </button>
          <nav className="hidden items-center gap-8 text-sm font-semibold text-slate-600 md:flex">
            <a href="#features" className="hover:text-slate-950">Product</a>
            <a href="#workflow" className="hover:text-slate-950">Workflow</a>
            <a href="#pricing" className="hover:text-slate-950">Pricing</a>
            <a href="#faq" className="hover:text-slate-950">FAQ</a>
          </nav>
          <div className="hidden items-center gap-2 md:flex">
            <button onClick={goLogin} className="rounded-xl px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-100">Login</button>
            <button onClick={goRegister} className="btn-primary">Get Started <ArrowRight size={16} /></button>
          </div>
          <button className="rounded-xl p-2 md:hidden" onClick={() => setMobileOpen(!mobileOpen)}>{mobileOpen ? <X /> : <Menu />}</button>
        </div>
        {mobileOpen && <div className="border-t border-slate-100 bg-white px-5 py-4 md:hidden"><div className="grid gap-2 text-sm font-semibold"><a href="#features" onClick={() => setMobileOpen(false)}>Product</a><a href="#workflow" onClick={() => setMobileOpen(false)}>Workflow</a><a href="#pricing" onClick={() => setMobileOpen(false)}>Pricing</a><a href="#faq" onClick={() => setMobileOpen(false)}>FAQ</a><button onClick={goLogin} className="mt-2 rounded-xl border border-slate-200 px-4 py-3 text-left">Login</button><button onClick={goRegister} className="btn-primary">Get Started <ArrowRight size={16}/></button></div></div>}
      </header>

      <main>
        <section className="relative mx-auto grid min-h-[760px] max-w-7xl items-center gap-14 px-5 pb-20 pt-36 lg:grid-cols-[1.05fr_.95fr] lg:px-8">
          <div>
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-indigo-100 bg-white/80 px-3.5 py-2 text-xs font-bold text-indigo-700 shadow-sm"><Sparkles size={14}/> Sales execution, with context</div>
            <h1 className="max-w-3xl text-5xl font-black leading-[1.02] tracking-[-0.04em] sm:text-6xl lg:text-7xl">Turn every lead into a <span className="bg-gradient-to-r from-indigo-600 via-violet-600 to-sky-500 bg-clip-text text-transparent">reason to reach out.</span></h1>
            <p className="mt-7 max-w-2xl text-lg leading-8 text-slate-600 sm:text-xl">SignalFlow AI helps sales teams decide who to contact now, why the timing matters, what to say, and what to do next — all in one focused workspace.</p>
            <div className="mt-9 flex flex-col gap-3 sm:flex-row"><button onClick={goRegister} className="btn-primary px-6 py-3.5 text-base">Start building your pipeline <ArrowRight size={18}/></button><button onClick={goLogin} className="btn-secondary px-6 py-3.5 text-base">Login to workspace</button></div>
            <div className="mt-8 flex flex-wrap gap-x-6 gap-y-3 text-sm text-slate-500"><span className="flex items-center gap-2"><Check size={15} className="text-emerald-500"/>Explainable lead scoring</span><span className="flex items-center gap-2"><Check size={15} className="text-emerald-500"/>Why Now context</span><span className="flex items-center gap-2"><Check size={15} className="text-emerald-500"/>Human-reviewed outreach</span></div>
          </div>
          <div className="relative">
            <div className="absolute -inset-8 rounded-[3rem] bg-gradient-to-br from-indigo-200/50 via-violet-100/40 to-sky-100/40 blur-3xl" />
            <div className="relative rounded-[2rem] border border-white/80 bg-slate-950 p-3 shadow-2xl shadow-indigo-200/60">
              <div className="overflow-hidden rounded-[1.45rem] border border-slate-800 bg-slate-900">
                <div className="flex items-center justify-between border-b border-slate-800 px-5 py-4"><div className="flex items-center gap-2"><span className="h-2 w-2 rounded-full bg-emerald-400"/><span className="text-xs font-semibold text-slate-300">SignalFlow workspace</span></div><span className="rounded-full bg-indigo-500/15 px-2 py-1 text-[10px] font-bold text-indigo-300">PRODUCT PREVIEW</span></div>
                <div className="grid gap-4 p-5 sm:grid-cols-2">
                  <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4"><div className="text-[10px] uppercase tracking-[.18em] text-slate-500">Priority lead</div><div className="mt-2 text-lg font-bold text-white">Aarav Mehta</div><div className="text-xs text-slate-500">Head of Sales · NovaForge</div><div className="mt-4 flex items-end justify-between"><div><div className="text-4xl font-black text-white">92</div><div className="text-[10px] uppercase tracking-widest text-slate-500">score / 100</div></div><span className="rounded-full bg-emerald-400/10 px-2.5 py-1 text-xs font-semibold text-emerald-300">High</span></div></div>
                  <div className="rounded-2xl border border-indigo-400/20 bg-indigo-500/10 p-4"><div className="text-[10px] uppercase tracking-[.18em] text-indigo-300">Why Now</div><p className="mt-3 text-sm leading-6 text-slate-200">Hiring signal + strong ICP fit create a timely reason to discuss sales productivity.</p><div className="mt-4 rounded-xl bg-white/5 p-3 text-xs text-slate-400">Recommended: lead with the hiring trigger.</div></div>
                  <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 sm:col-span-2"><div className="flex items-center justify-between"><div><div className="text-[10px] uppercase tracking-[.18em] text-slate-500">Outreach draft</div><div className="mt-2 text-sm font-semibold text-white">A timely idea for NovaForge</div></div><span className="rounded-lg bg-white/5 px-2 py-1 text-[10px] text-slate-400">AI + review</span></div><p className="mt-3 text-sm leading-6 text-slate-400">Hi Aarav, I noticed NovaForge is expanding the sales team…</p><div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-800"><div className="h-full w-4/5 rounded-full bg-gradient-to-r from-indigo-500 to-sky-400"/></div></div>
                  <div className="grid grid-cols-3 gap-3 sm:col-span-2"><MiniMetric label="Example sends" value="48"/><MiniMetric label="Replies" value="12"/><MiniMetric label="Meetings" value="6"/></div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="features" className="mx-auto max-w-7xl scroll-mt-24 px-5 py-24 lg:px-8"><div className="max-w-2xl"><p className="text-sm font-bold uppercase tracking-[.18em] text-indigo-600">Built around the sales decision</p><h2 className="mt-3 text-4xl font-black tracking-tight sm:text-5xl">Less tab switching. More useful context.</h2><p className="mt-5 text-lg leading-8 text-slate-500">Borrow familiar patterns from modern sales platforms while keeping the MVP focused on the decision layer: why this lead, why now, and what should I send?</p></div><div className="mt-12 grid gap-5 md:grid-cols-2 xl:grid-cols-4">{features.map(({icon:Icon,title,text})=><div key={title} className="group rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-xl hover:shadow-indigo-100"><div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600 transition group-hover:bg-slate-950 group-hover:text-white"><Icon size={22}/></div><h3 className="mt-6 text-lg font-bold">{title}</h3><p className="mt-2 leading-7 text-slate-500">{text}</p></div>)}</div></section>

        <section id="workflow" className="scroll-mt-24 bg-slate-950 py-24 text-white"><div className="mx-auto max-w-7xl px-5 lg:px-8"><div className="max-w-2xl"><p className="text-sm font-bold uppercase tracking-[.18em] text-indigo-300">One clear workflow</p><h2 className="mt-3 text-4xl font-black tracking-tight sm:text-5xl">From raw lead list to measurable next action.</h2></div><div className="mt-12 grid gap-3 md:grid-cols-2 xl:grid-cols-3">{workflow.map(([num,title,text])=><div key={num} className="rounded-3xl border border-slate-800 bg-white/[.03] p-6 hover:border-indigo-400/40"><div className="text-xs font-black tracking-[.2em] text-indigo-300">{num}</div><h3 className="mt-4 text-xl font-bold">{title}</h3><p className="mt-2 leading-7 text-slate-400">{text}</p></div>)}</div><div className="mt-12 rounded-3xl border border-indigo-400/20 bg-gradient-to-r from-indigo-500/15 to-sky-500/10 p-8"><div className="flex flex-col items-start justify-between gap-6 md:flex-row md:items-center"><div><div className="text-xl font-bold">Lead → Signal → Reason → Message → Sequence → Result</div><p className="mt-2 text-slate-400">A compact mental model for the entire product.</p></div><button onClick={goRegister} className="btn bg-white text-slate-950 hover:bg-slate-100">Explore the workspace <ArrowRight size={16}/></button></div></div></div></section>

        <section id="pricing" className="mx-auto max-w-7xl scroll-mt-24 px-5 py-24 lg:px-8"><div className="flex flex-col justify-between gap-5 md:flex-row md:items-end"><div><p className="text-sm font-bold uppercase tracking-[.18em] text-indigo-600">Simple product model</p><h2 className="mt-3 text-4xl font-black tracking-tight sm:text-5xl">Start small. Scale with your workflow.</h2></div><Link to={user ? '/plans' : '/register'} className="btn-secondary">View plans <ArrowRight size={16}/></Link></div><div className="mt-12 grid gap-5 lg:grid-cols-4">{[['Free','100 leads','1 campaign'],['Starter','1,000 leads','5 campaigns'],['Professional','10,000 leads','25 campaigns'],['Business','Custom limits','Team controls']].map(([name,a,b])=><div key={name} className={`rounded-3xl border bg-white p-6 shadow-sm ${name==='Professional'?'border-indigo-200 ring-2 ring-indigo-100':'border-slate-200'}`}><div className="flex items-center justify-between"><h3 className="text-xl font-black">{name}</h3>{name==='Professional'&&<span className="badge bg-indigo-50 text-indigo-700">Popular</span>}</div><div className="mt-6 space-y-3 text-sm text-slate-600"><div className="flex gap-2"><Check size={16} className="text-emerald-500"/>{a}</div><div className="flex gap-2"><Check size={16} className="text-emerald-500"/>{b}</div><div className="flex gap-2"><Check size={16} className="text-emerald-500"/>AI-assisted outreach</div></div></div>)}</div></section>

        <section id="faq" className="mx-auto max-w-4xl scroll-mt-24 px-5 py-24 lg:px-8"><div className="text-center"><p className="text-sm font-bold uppercase tracking-[.18em] text-indigo-600">FAQ</p><h2 className="mt-3 text-4xl font-black tracking-tight">Questions, answered.</h2></div><div className="mt-10 divide-y overflow-hidden rounded-3xl border border-slate-200 bg-white">{faqs.map(([q,a],i)=><button key={q} onClick={()=>setOpenFaq(openFaq===i?-1:i)} className="w-full px-6 py-5 text-left"><div className="flex items-center justify-between gap-5"><span className="font-bold">{q}</span><ChevronDown size={18} className={`shrink-0 text-slate-400 transition ${openFaq===i?'rotate-180':''}`}/></div>{openFaq===i&&<p className="mt-3 max-w-3xl pr-6 text-sm leading-7 text-slate-500">{a}</p>}</button>)}</div></section>

        <section className="mx-auto max-w-7xl px-5 pb-24 lg:px-8"><div className="overflow-hidden rounded-[2.5rem] bg-slate-950 px-7 py-12 text-white shadow-2xl shadow-indigo-200 sm:px-10 md:flex md:items-center md:justify-between md:gap-10"><div><p className="text-sm font-bold uppercase tracking-[.18em] text-indigo-300">Ready to focus?</p><h2 className="mt-3 max-w-2xl text-4xl font-black tracking-tight">Give your sales team a clearer next move.</h2><p className="mt-4 max-w-xl leading-7 text-slate-400">See which leads matter, understand the signal, draft the message, and keep the workflow moving.</p></div><div className="mt-8 flex shrink-0 flex-col gap-3 sm:flex-row md:mt-0"><button onClick={goRegister} className="btn bg-white px-6 py-3.5 text-slate-950 hover:bg-slate-100">Get Started <ArrowRight size={17}/></button><button onClick={goLogin} className="btn border border-white/15 bg-white/5 px-6 py-3.5 text-white hover:bg-white/10">Login</button></div></div></section>
      </main>

      <footer className="border-t border-slate-200 bg-white"><div className="mx-auto flex max-w-7xl flex-col gap-4 px-5 py-8 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between lg:px-8"><div className="font-bold text-slate-900">SignalFlow<span className="text-indigo-600"> AI</span></div><div>AI-assisted sales execution • Assessment MVP</div><div>© 2026 SignalFlow AI</div></div></footer>
    </div>
  )
}

function MiniMetric({ label, value }) { return <div className="rounded-xl border border-slate-800 bg-slate-950 p-3"><div className="text-[10px] uppercase tracking-wider text-slate-500">{label}</div><div className="mt-1 text-xl font-black text-white">{value}</div></div> }
