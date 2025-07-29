import React from 'react'
import { Routes, Route } from 'react-router-dom'
import LoginPage from './Pages/Login'

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
    </Routes>
  )
}

export default AppRoutes