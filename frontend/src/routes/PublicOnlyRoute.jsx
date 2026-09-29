import { Navigate, Outlet, useLocation } from 'react-router-dom'
import Loading from '../components/Loading'
import { useAuth } from '../context/AuthContext'

export default function PublicOnlyRoute() {
  const { user, loading } = useAuth()
  const location = useLocation()
  if (loading) return <Loading />
  if (user) return <Navigate to="/dashboard" replace state={{ from: location.pathname }} />
  return <Outlet />
}
