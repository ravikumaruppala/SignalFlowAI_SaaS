import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { ArrowLeft, ArrowRight, Bot, CheckCircle2, Eye, EyeOff, ShieldCheck } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export function Login() {
  const [form, setForm] = useState({ email: '', password: '', remember_me: false })
  const { login, error } = useAuth()
  const nav = useNavigate()
  const loc = useLocation()
  const [busy, setBusy] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  async function submit(e) {
    e.preventDefault()
    setBusy(true)
    if (await login(form.email, form.password, form.remember_me)) nav(loc.state?.from || '/dashboard', { replace: true })
    setBusy(false)
  }

  return <AuthShell title="Welcome back" subtitle="Turn your lead list into the next best sales action.">
    <form className="space-y-4" onSubmit={submit}>
      <Field label="Email" type="email" value={form.email} onChange={v => setForm({ ...form, email: v })}/>
      <PasswordField label="Password" value={form.password} show={showPassword} setShow={setShowPassword} onChange={v => setForm({ ...form, password: v })}/>
      <div className="flex items-center justify-between gap-4"><label className="flex items-center gap-2 text-sm text-slate-600"><input type="checkbox" checked={form.remember_me} onChange={e => setForm({ ...form, remember_me: e.target.checked })} className="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"/> Remember me</label><Link className="text-sm font-semibold text-indigo-600 hover:text-indigo-700" to="/forgot-password">Forgot password?</Link></div>
      {error && <div className="rounded-xl bg-red-50 p-3 text-sm text-red-700">{typeof error === 'string' ? error : 'Unable to sign in.'}</div>}
      <button className="btn-primary w-full" disabled={busy}>{busy ? 'Signing in…' : 'Sign in'}<ArrowRight size={16}/></button>
      <div className="text-center text-sm text-slate-500">New here? <Link className="font-semibold text-indigo-600" to="/register">Create account</Link></div>
    </form>
  </AuthShell>
}

export function Register() {
  const [form, setForm] = useState({ email: '', full_name: '', password: '', role: 'sales_rep', team_name: 'Demo Sales Team' })
  const { register, error } = useAuth()
  const nav = useNavigate()
  const [busy, setBusy] = useState(false)
  async function submit(e) { e.preventDefault(); setBusy(true); if (await register(form)) nav('/dashboard'); setBusy(false) }
  return <AuthShell title="Create your workspace" subtitle="Start with a clean, role-aware sales workspace."><form className="space-y-4" onSubmit={submit}><Field label="Full name" value={form.full_name} onChange={v => setForm({ ...form, full_name: v })}/><Field label="Email" type="email" value={form.email} onChange={v => setForm({ ...form, email: v })}/><Field label="Password" type="password" value={form.password} onChange={v => setForm({ ...form, password: v })}/><Field label="Team" value={form.team_name} onChange={v => setForm({ ...form, team_name: v })}/><label className="block"><span className="mb-1.5 block text-sm font-medium text-slate-700">Role</span><select className="input" value={form.role} onChange={e => setForm({ ...form, role: e.target.value })}><option value="sales_rep">Sales Representative</option><option value="manager">Sales Manager</option></select></label>{error&&<div className="rounded-xl bg-red-50 p-3 text-sm text-red-700">{typeof error==='string'?error:'Unable to register.'}</div>}<button className="btn-primary w-full" disabled={busy}>{busy?'Creating…':'Create account'}<ArrowRight size={16}/></button><div className="text-center text-sm text-slate-500">Already registered? <Link className="font-semibold text-indigo-600" to="/login">Sign in</Link></div></form></AuthShell>
}

function Field({ label, type = 'text', value, onChange }) { return <label className="block"><span className="mb-1.5 block text-sm font-medium text-slate-700">{label}</span><input className="input" type={type} value={value} onChange={e => onChange(e.target.value)} required/></label> }
function PasswordField({ label, value, onChange, show, setShow }) { return <label className="block"><span className="mb-1.5 block text-sm font-medium text-slate-700">{label}</span><div className="relative"><input className="input pr-11" type={show ? 'text' : 'password'} value={value} onChange={e => onChange(e.target.value)} required/><button type="button" className="absolute right-3 top-2.5 text-slate-400 hover:text-slate-700" onClick={() => setShow(!show)}>{show?<EyeOff size={18}/>:<Eye size={18}/>}</button></div></label> }

function AuthShell({ title, subtitle, children }) { return <div className="grid min-h-screen bg-slate-50 lg:grid-cols-[.95fr_1.05fr]"><div className="hidden bg-slate-950 px-10 py-12 text-white lg:flex lg:flex-col lg:justify-between"><div><Link to="/" className="flex items-center gap-2 text-xl font-extrabold"><span className="flex h-9 w-9 items-center justify-center rounded-xl bg-white/10"><Bot size={18} className="text-indigo-300"/></span>SignalFlow AI</Link><h1 className="mt-16 max-w-xl text-5xl font-black leading-[1.05] tracking-tight">Lead → Signal → Reason → Message → Sequence → Result.</h1><p className="mt-6 max-w-xl text-lg leading-8 text-slate-400">A focused workspace for prioritizing the right prospect and turning a signal into an actionable outreach sequence.</p></div><div className="space-y-3"><div className="flex items-center gap-2 text-sm text-slate-400"><ShieldCheck size={16} className="text-emerald-400"/>Your password stays inside Django authentication.</div><div className="grid gap-4 sm:grid-cols-3">{['Explainable scoring','Why Now signals','Reviewed outreach'].map(x=><div key={x} className="rounded-2xl border border-slate-800 p-4 text-sm text-slate-300"><CheckCircle2 size={16} className="mb-2 text-emerald-400"/>{x}</div>)}</div></div></div><div className="flex items-center justify-center p-6 md:p-10"><div className="w-full max-w-md"><Link to="/" className="mb-7 inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-slate-900"><ArrowLeft size={15}/>Back to home</Link><h2 className="text-3xl font-black tracking-tight">{title}</h2><p className="mt-2 text-slate-500">{subtitle}</p><div className="mt-8">{children}</div></div></div></div> }
