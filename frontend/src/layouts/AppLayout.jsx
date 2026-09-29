import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { BarChart3, Bot, ChevronDown, Inbox, LayoutDashboard, ListChecks, LogOut, Menu, Megaphone, Settings, Users, X } from 'lucide-react'
import { useState } from 'react'
import { useAuth } from '../context/AuthContext'

const items = [
  ['/dashboard', 'Dashboard', LayoutDashboard], ['/leads','Leads',Users], ['/campaigns','Campaigns',Megaphone], ['/sequences','Sequences',ListChecks], ['/inbox','Inbox',Inbox], ['/analytics','Analytics',BarChart3], ['/plans','Plans',Bot], ['/profile','Profile',Settings]
]
export default function AppLayout(){
  const [open,setOpen]=useState(false); const {user,logout}=useAuth(); const nav=useNavigate(); const loc=useLocation();
  const handleLogout=async()=>{await logout();nav('/login')}
  return <div className="min-h-screen bg-slate-50">
    <aside className={`fixed inset-y-0 left-0 z-40 w-64 border-r border-slate-800 bg-slate-950 text-white transition-transform md:translate-x-0 ${open?'translate-x-0':'-translate-x-full'}`}>
      <div className="flex h-16 items-center justify-between border-b border-slate-800 px-5"><div><div className="text-lg font-extrabold tracking-tight">SignalFlow<span className="text-indigo-400"> AI</span></div><div className="text-[10px] uppercase tracking-[0.22em] text-slate-500">Sales execution</div></div><button className="md:hidden" onClick={()=>setOpen(false)}><X size={20}/></button></div>
      <nav className="space-y-1 p-3">{items.map(([to,label,Icon])=><NavLink key={to} to={to} end={to==='/dashboard'} onClick={()=>setOpen(false)} className={({isActive})=>`flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium ${isActive?'bg-white/10 text-white':'text-slate-400 hover:bg-white/5 hover:text-white'}`}><Icon size={18}/>{label}</NavLink>)}</nav>
      {user?.role==='admin' && <div className="mx-3 mt-4 rounded-xl border border-slate-800 p-3 text-xs text-slate-400"><div className="font-semibold text-slate-200">Admin access</div><a href="http://localhost:8000/admin/" target="_blank" rel="noreferrer" className="mt-1 inline-block text-indigo-400 hover:underline">Open Django Admin ↗</a></div>}
      <div className="absolute bottom-0 left-0 right-0 border-t border-slate-800 p-3"><button onClick={handleLogout} className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-slate-400 hover:bg-white/5 hover:text-white"><LogOut size={18}/>Logout</button></div>
    </aside>
    <div className="md:pl-64"><header className="sticky top-0 z-30 border-b border-slate-200 bg-white/95 backdrop-blur"><div className="flex h-16 items-center justify-between px-4 md:px-8"><button className="md:hidden" onClick={()=>setOpen(true)}><Menu/></button><div><p className="text-xs uppercase tracking-[0.2em] text-slate-400">Workspace</p><h1 className="text-base font-bold">{items.find(([to])=>to===loc.pathname)?.[1] || 'SignalFlow AI'}</h1></div><div className="flex items-center gap-3"><div className="hidden text-right sm:block"><div className="text-sm font-semibold">{user?.full_name}</div><div className="text-xs text-slate-400">{user?.role_label}</div></div><div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-900 text-sm font-bold text-white">{(user?.full_name||'U').split(' ').map(x=>x[0]).slice(0,2).join('')}</div><ChevronDown size={16} className="text-slate-400"/></div></div></header><main className="p-4 md:p-8"><Outlet/></main></div>
  </div>
}
