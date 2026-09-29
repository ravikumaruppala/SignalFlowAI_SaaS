import { Check, CreditCard, Loader2, Sparkles, ShieldCheck, ReceiptText } from 'lucide-react'
import { useEffect, useState } from 'react'
import api, { apiError } from '../api/client'
import Toast from '../components/Toast'
import { useAuth } from '../context/AuthContext'

const plans = [
  {
    code: 'free',
    name: 'Free',
    price: 0,
    features: ['100 leads', '1 campaign', '10 AI generations / month'],
    purpose: 'Product discovery',
  },
  {
    code: 'starter',
    name: 'Starter',
    price: 999,
    features: ['1,000 leads', '5 campaigns', '100 AI generations / month', '1 seat'],
    purpose: 'Small sales teams',
  },
  {
    code: 'professional',
    name: 'Professional',
    price: 2499,
    features: ['10,000 leads', '25 campaigns', '500 AI generations / month', '5 seats'],
    purpose: 'Growing teams',
    highlighted: true,
  },
  {
    code: 'business',
    name: 'Business',
    price: null,
    features: ['Custom limits', 'Team controls', 'Integrations', 'Priority support'],
    purpose: 'Larger teams',
  },
]

function loadRazorpayScript() {
  return new Promise((resolve) => {
    if (window.Razorpay) return resolve(true)
    const existing = document.querySelector('script[data-razorpay-checkout="true"]')
    if (existing) {
      existing.addEventListener('load', () => resolve(true), { once: true })
      existing.addEventListener('error', () => resolve(false), { once: true })
      return
    }
    const script = document.createElement('script')
    script.src = 'https://checkout.razorpay.com/v1/checkout.js'
    script.async = true
    script.dataset.razorpayCheckout = 'true'
    script.onload = () => resolve(true)
    script.onerror = () => resolve(false)
    document.body.appendChild(script)
  })
}

export default function Plans() {
  const { user } = useAuth()
  const [subscription, setSubscription] = useState(null)
  const [history, setHistory] = useState([])
  const [loadingPlan, setLoadingPlan] = useState('')
  const [toast, setToast] = useState('')
  const [error, setError] = useState('')

  async function loadBilling() {
    try {
      const [sub, payments] = await Promise.all([
        api.get('/payments/subscription/'),
        api.get('/payments/history/'),
      ])
      setSubscription(sub.data)
      setHistory(payments.data || [])
    } catch (e) {
      setError(apiError(e))
    }
  }

  useEffect(() => { loadBilling() }, [])

  async function handlePayment(plan) {
    setError('')
    setLoadingPlan(plan.code)
    try {
      const loaded = await loadRazorpayScript()
      if (!loaded) throw new Error('Razorpay Checkout could not be loaded. Check your internet connection and try again.')

      const orderResponse = await api.post('/payments/create-order/', { plan_code: plan.code })
      const { payment, key_id, name, description } = orderResponse.data

      const options = {
        key: key_id,
        amount: payment.amount,
        currency: payment.currency,
        name,
        description,
        order_id: payment.razorpay_order_id,
        handler: async (response) => {
          try {
            await api.post('/payments/verify/', {
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
            })
            await loadBilling()
            setToast(`${plan.name} payment verified. Your plan is now active for 30 days.`)
          } catch (e) {
            setError(apiError(e))
          } finally {
            setLoadingPlan('')
          }
        },
        prefill: {
          name: user?.full_name || '',
          email: user?.email || '',
        },
        notes: {
          plan: plan.code,
          application: 'SignalFlow AI',
        },
        theme: { color: '#4f46e5' },
        modal: { ondismiss: () => setLoadingPlan('') },
      }

      const razorpay = new window.Razorpay(options)
      razorpay.on('payment.failed', (response) => {
        setError(response?.error?.description || 'Payment failed. Please try again.')
        setLoadingPlan('')
      })
      razorpay.open()
    } catch (e) {
      setError(apiError(e))
      setLoadingPlan('')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-2 text-indigo-600">
          <CreditCard size={18} />
          <span className="text-sm font-semibold">Razorpay payment gateway</span>
        </div>
        <h2 className="mt-1 text-2xl font-black">Plans & billing</h2>
        <p className="mt-2 max-w-3xl text-slate-500">
          Paid plans use Razorpay Standard Checkout in test mode. Prices below are illustrative assessment pricing, not market claims.
        </p>
      </div>

      <div className="card flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">Current plan</div>
          <div className="mt-1 text-xl font-black">{subscription?.plan_label || 'Free'}</div>
          <div className="mt-1 text-sm text-slate-500">
            {subscription?.ends_at ? `Active until ${new Date(subscription.ends_at).toLocaleDateString()}` : 'No paid subscription is active.'}
          </div>
        </div>
        <div className="flex items-center gap-2 rounded-xl bg-emerald-50 px-3 py-2 text-sm font-semibold text-emerald-700">
          <ShieldCheck size={17} /> Secure server-side verification
        </div>
      </div>

      {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

      <div className="grid gap-5 lg:grid-cols-4">
        {plans.map((plan) => {
          const isCurrent = subscription?.plan_code === plan.code
          return (
            <div key={plan.code} className={`card flex flex-col p-5 ${plan.highlighted ? 'border-indigo-200 ring-2 ring-indigo-100' : ''}`}>
              <div className="flex items-center justify-between">
                <div className="text-lg font-black">{plan.name}</div>
                {plan.highlighted && <span className="badge bg-indigo-50 text-indigo-700">Popular</span>}
              </div>
              <div className="mt-4 flex items-end gap-1">
                {plan.price === null ? <span className="text-2xl font-black">Custom</span> : <><span className="text-3xl font-black">₹{plan.price.toLocaleString('en-IN')}</span>{plan.price > 0 && <span className="pb-1 text-sm text-slate-400">/30 days</span>}</>}
              </div>
              <div className="mt-5 flex-1 space-y-3">
                {plan.features.map((feature) => <div key={feature} className="flex gap-2 text-sm text-slate-600"><Check size={16} className="mt-0.5 text-emerald-500" />{feature}</div>)}
              </div>
              <div className="mt-6 rounded-xl bg-slate-50 p-3 text-xs text-slate-500">{plan.purpose}</div>

              {plan.code === 'free' && <button className="btn-secondary mt-4 w-full" disabled>{isCurrent ? 'Current plan' : 'Free plan'}</button>}
              {plan.code === 'business' && <button className="btn-secondary mt-4 w-full" onClick={() => setToast('Business plan is custom. Use the assessment roadmap for future enterprise billing.')}>Contact Sales</button>}
              {plan.code !== 'free' && plan.code !== 'business' && (
                <button className="btn-primary mt-4 w-full" onClick={() => handlePayment(plan)} disabled={loadingPlan === plan.code || isCurrent}>
                  {loadingPlan === plan.code ? <><Loader2 size={16} className="animate-spin" />Opening checkout...</> : isCurrent ? 'Current plan' : <>Pay with Razorpay <CreditCard size={16} /></>}
                </button>
              )}
            </div>
          )
        })}
      </div>

      <div className="card p-5">
        <div className="flex items-center gap-2 font-bold"><ReceiptText size={17} />Recent payments</div>
        <p className="mt-1 text-sm text-slate-500">Payment records are persisted in MySQL and can be reviewed from Django Admin.</p>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[720px] text-left text-sm">
            <thead><tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400"><th className="px-3 py-3">Date</th><th className="px-3 py-3">Plan</th><th className="px-3 py-3">Amount</th><th className="px-3 py-3">Status</th><th className="px-3 py-3">Razorpay Order</th></tr></thead>
            <tbody>
              {history.length === 0 ? <tr><td colSpan="5" className="px-3 py-8 text-center text-slate-400">No payments yet.</td></tr> : history.map((item) => (
                <tr key={item.id} className="border-b border-slate-100 last:border-0">
                  <td className="px-3 py-3 text-slate-500">{new Date(item.created_at).toLocaleString()}</td>
                  <td className="px-3 py-3 font-semibold">{item.plan_label}</td>
                  <td className="px-3 py-3">₹{Number(item.amount_rupees).toLocaleString('en-IN')}</td>
                  <td className="px-3 py-3"><span className={`badge ${item.status === 'verified' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}`}>{item.status}</span></td>
                  <td className="px-3 py-3 font-mono text-xs text-slate-500">{item.razorpay_order_id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="rounded-xl border border-indigo-100 bg-indigo-50 p-4 text-sm text-indigo-900">
        <strong>Demo note:</strong> use Razorpay <strong>test-mode</strong> keys. The secret key stays only in Django; React receives only the public key ID and server-created order ID.
      </div>
      <Toast message={toast} />
    </div>
  )
}
