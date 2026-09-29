import { Navigate } from 'react-router-dom'
import Loading from '../components/Loading'
import { useAuth } from '../context/AuthContext'
export default function ProtectedRoute({ children }) { const {user,loading}=useAuth(); if(loading) return <Loading/>; return user ? children : <Navigate to="/login" replace/> }
