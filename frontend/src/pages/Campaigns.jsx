import { useEffect, useState } from 'react'
import { ArrowRight, Megaphone, Pencil, Play, Plus, Trash2, UserPlus } from 'lucide-react'
import { Link } from 'react-router-dom'
import api, { apiError } from '../api/client'
import Modal from '../components/Modal'
import Badge from '../components/Badge'
import Toast from '../components/Toast'

const emptyForm={name:'',description:'',status:'draft'}
export default function Campaigns(){
  const [items,setItems]=useState([]); const [leads,setLeads]=useState([]);
  const [open,setOpen]=useState(false); const [assignOpen,setAssignOpen]=useState(false);
  const [selected,setSelected]=useState(null); const [editing,setEditing]=useState(null);
  const [form,setForm]=useState(emptyForm); const [chosen,setChosen]=useState([]);
  const [toast,setToast]=useState(''); const [error,setError]=useState('');
  async function load(){try{const [c,l]=await Promise.all([api.get('/campaigns/'),api.get('/leads/')]);setItems(c.data);setLeads(l.data)}catch(e){setError(apiError(e))}}
  useEffect(()=>{load()},[])
  function create(){setEditing(null);setForm({...emptyForm});setOpen(true)}
  function edit(c){setEditing(c);setForm({name:c.name,description:c.description||'',status:c.status});setOpen(true)}
  async function save(e){e.preventDefault();try{if(editing) await api.patch(`/campaigns/${editing.id}/`,form); else await api.post('/campaigns/',form);setOpen(false);setToast(editing?'Campaign updated':'Campaign created');load()}catch(e){setError(apiError(e))}}
  async function remove(c){if(!confirm(`Delete ${c.name}?`))return;try{await api.delete(`/campaigns/${c.id}/`);setToast('Campaign deleted');load()}catch(e){setError(apiError(e))}}
  async function assign(){try{const r=await api.post(`/campaigns/${selected.id}/leads/`,{lead_ids:chosen});setAssignOpen(false);setChosen([]);setToast(`${r.data.created} lead(s) assigned`);load()}catch(e){setError(apiError(e))}}
  async function simulate(c,event){try{const r=await api.post(`/campaigns/${c.id}/simulate/`,{event});setToast(`${r.data.created} ${event} event(s) recorded`);load()}catch(e){setError(apiError(e))}}
  return <div className="space-y-6">
    <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end"><div><h2 className="text-2xl font-black">Campaigns</h2><p className="text-slate-500">Create, assign, sequence and simulate campaigns.</p></div><button className="btn-primary" onClick={create}><Plus size={16}/>Create campaign</button></div>
    {error&&<div className="rounded-xl bg-red-50 p-4 text-sm text-red-700">{error}</div>}
    <div className="grid gap-5 lg:grid-cols-2">
      {items.map(c=><div className="card p-5" key={c.id}>
        <div className="flex items-start justify-between gap-3"><div><div className="flex items-center gap-2"><Megaphone size={17} className="text-indigo-600"/><h3 className="font-bold">{c.name}</h3></div><p className="mt-2 text-sm text-slate-500">{c.description || 'No description.'}</p></div><Badge tone={c.status==='active'?'green':c.status==='paused'?'amber':'slate'}>{c.status}</Badge></div>
        <div className="mt-5 grid grid-cols-4 gap-2"><Mini title="Leads" value={c.stats?.leads ?? c.campaign_leads.length}/><Mini title="Sends" value={c.stats?.sends ?? 0}/><Mini title="Replies" value={c.stats?.replies ?? 0}/><Mini title="Meetings" value={c.stats?.meetings ?? 0}/></div>
        <div className="mt-5 border-t border-slate-100 pt-4"><div className="text-xs font-semibold uppercase tracking-wide text-slate-400">3-step sequence</div><div className="mt-2 grid gap-2 sm:grid-cols-3">{c.sequence_steps.map(s=><div key={s.id} className="rounded-xl bg-slate-50 p-3"><div className="text-xs font-bold">Day {s.day_offset}</div><div className="mt-1 line-clamp-2 text-xs text-slate-500">{s.subject_template}</div></div>)}</div></div>
        <div className="mt-5 flex flex-wrap gap-2"><button className="btn-secondary" onClick={()=>edit(c)}><Pencil size={15}/>Edit</button><button className="btn-secondary" onClick={()=>remove(c)}><Trash2 size={15}/>Delete</button><button className="btn-secondary" onClick={()=>{setSelected(c);setAssignOpen(true)}}><UserPlus size={15}/>Assign leads</button><Link className="btn-secondary" to="/sequences">Sequence <ArrowRight size={15}/></Link><button className="btn-secondary" onClick={()=>simulate(c,'send')}><Play size={15}/>Simulate send</button><button className="btn-secondary" onClick={()=>simulate(c,'reply')}>Reply</button><button className="btn-secondary" onClick={()=>simulate(c,'meeting')}>Meeting</button></div>
      </div>)}
      {items.length===0&&<div className="card p-12 text-center text-slate-400 lg:col-span-2">No campaigns yet. Create one to start.</div>}
    </div>
    <Modal open={open} title={editing?'Edit campaign':'Create campaign'} onClose={()=>setOpen(false)}><form className="space-y-4" onSubmit={save}><label className="block"><span className="mb-1 block text-sm font-medium">Name</span><input className="input" required value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/></label><label className="block"><span className="mb-1 block text-sm font-medium">Description</span><textarea className="input min-h-28" value={form.description} onChange={e=>setForm({...form,description:e.target.value})}/></label><label className="block"><span className="mb-1 block text-sm font-medium">Status</span><select className="input" value={form.status} onChange={e=>setForm({...form,status:e.target.value})}><option value="draft">Draft</option><option value="active">Active</option><option value="paused">Paused</option><option value="completed">Completed</option></select></label><button className="btn-primary w-full">{editing?'Save changes':'Create campaign'}</button></form></Modal>
    <Modal open={assignOpen} title={`Assign leads — ${selected?.name||''}`} onClose={()=>setAssignOpen(false)}><div className="space-y-2">{leads.map(l=><label key={l.id} className="flex items-center gap-3 rounded-xl border border-slate-100 p-3 hover:bg-slate-50"><input type="checkbox" checked={chosen.includes(l.id)} onChange={e=>setChosen(e.target.checked?[...chosen,l.id]:chosen.filter(x=>x!==l.id))}/><div><div className="text-sm font-semibold">{l.name}</div><div className="text-xs text-slate-400">{l.company} · {l.score}</div></div></label>)}<button className="btn-primary mt-3 w-full" onClick={assign}>Assign selected</button></div></Modal>
    <Toast message={toast}/>
  </div>
}
function Mini({title,value}){return <div className="rounded-xl bg-slate-50 p-3"><div className="text-xs text-slate-400">{title}</div><div className="mt-1 font-bold capitalize">{value}</div></div>}
