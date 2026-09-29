import { useEffect, useState } from 'react'
import { ArrowLeft, ArrowRight, CheckCircle2, MailCheck, ShieldCheck } from 'lucide-react'
import { Link } from 'react-router-dom'
import api, { apiError, initCsrf } from '../api/client'

export default function ForgotPassword() {
  const [email, setEmail] = useState('')
  const [otp, setOtp] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [step, setStep] = useState('request')
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [seconds, setSeconds] = useState(0)

  useEffect(() => { if (!seconds) return undefined; const timer = setInterval(() => setSeconds(s => Math.max(0, s - 1)), 1000); return () => clearInterval(timer) }, [seconds])

  async function requestOtp(e) {
    e.preventDefault(); setError(''); setMessage(''); setBusy(true)
    try { await initCsrf(); const r = await api.post('/auth/password/request-otp/', { email }); setMessage(r.data.detail); setStep('reset'); setSeconds(60) } catch (e) { setError(apiError(e)) } finally { setBusy(false) }
  }

  async function resetPassword(e) {
    e.preventDefault(); setError(''); setMessage('');
    if (password !== confirm) { setError('Passwords do not match.'); return }
    setBusy(true)
    try { await initCsrf(); const r = await api.post('/auth/password/reset/', { email, otp, new_password: password }); setMessage(r.data.detail); setStep('done') } catch (e) { setError(apiError(e)) } finally { setBusy(false) }
  }

  return <div className="min-h-screen bg-slate-950 p-5"><div className="mx-auto flex min-h-[calc(100vh-2.5rem)] max-w-6xl items-center justify-center"><div className="grid w-full overflow-hidden rounded-[2rem] border border-white/10 bg-white shadow-2xl lg:grid-cols-[.85fr_1.15fr]"><div className="hidden bg-gradient-to-br from-indigo-600 via-violet-600 to-slate-950 p-10 text-white lg:block"><Link to="/" className="inline-flex items-center gap-2 font-black"><span className="rounded-xl bg-white/15 p-2"><MailCheck size={17}/></span>SignalFlow AI</Link><h1 className="mt-20 text-4xl font-black leading-tight">Reset your password without leaving your workflow.</h1><p className="mt-5 leading-7 text-indigo-100/80">We send a short-lived one-time code to the account email, then let you choose a new password.</p><div className="mt-10 space-y-4 text-sm">{['OTP expires after 10 minutes','Maximum 5 verification attempts','Passwords are stored using Django hashing'].map(x=><div key={x} className="flex gap-3"><CheckCircle2 size={17} className="mt-0.5 text-emerald-300"/>{x}</div>)}</div></div><div className="p-7 sm:p-10"><Link to="/login" className="inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-slate-900"><ArrowLeft size={15}/>Back to login</Link><div className="mt-8 max-w-md"><div className="mb-2 flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600"><ShieldCheck size={22}/></div><h2 className="text-3xl font-black tracking-tight">Forgot password?</h2><p className="mt-2 text-slate-500">{step==='request'?'Enter your account email and we’ll send a verification code.':step==='reset'?'Enter the OTP from your email and choose a new password.':'Your password has been reset successfully.'}</p>{step==='request'&&<form className="mt-8 space-y-4" onSubmit={requestOtp}><Field label="Account email" type="email" value={email} onChange={setEmail}/>{error&&<Error text={error}/>}<button className="btn-primary w-full" disabled={busy}>{busy?'Sending OTP…':'Send OTP'}<ArrowRight size={16}/></button></form>}{step==='reset'&&<form className="mt-8 space-y-4" onSubmit={resetPassword}><div className="rounded-xl bg-indigo-50 p-3 text-sm text-indigo-800">{message}</div><Field label="6-digit OTP" value={otp} onChange={setOtp} maxLength={6}/><Field label="New password" type="password" value={password} onChange={setPassword}/><Field label="Confirm password" type="password" value={confirm} onChange={setConfirm}/>{error&&<Error text={error}/>}<button className="btn-primary w-full" disabled={busy}>{busy?'Resetting…':'Reset password'}<ArrowRight size={16}/></button><button type="button" disabled={seconds>0||busy} onClick={requestOtp} className="btn-secondary w-full">{seconds>0?`Resend OTP in ${seconds}s`:'Resend OTP'}</button></form>}{step==='done'&&<div className="mt-8 space-y-4"><div className="rounded-2xl bg-emerald-50 p-5 text-emerald-800"><CheckCircle2 className="mb-2"/> {message}</div><Link className="btn-primary w-full" to="/login">Go to login <ArrowRight size={16}/></Link></div>}</div></div></div></div></div>
}
function Field({label,type='text',value,onChange,maxLength}){return <label className="block"><span className="mb-1.5 block text-sm font-medium text-slate-700">{label}</span><input className="input" type={type} value={value} maxLength={maxLength} onChange={e=>onChange(e.target.value)} required/></label>}
function Error({text}){return <div className="rounded-xl bg-red-50 p-3 text-sm text-red-700">{typeof text==='string'?text:'Unable to complete request.'}</div>}
