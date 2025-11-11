import React, {useEffect, useState} from 'react'

export default function App(){
  const [employees, setEmployees] = useState([])
  const [form, setForm] = useState({emp_code:'', first_name:'', last_name:'', email:'', post:'GR-A', base_pay:''})
  const api = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const fetchEmployees = ()=> {
    fetch(api + '/employees/')
      .then(r=>r.json()).then(data=>setEmployees(data))
      .catch(e=>console.error(e))
  }

  useEffect(()=>{ fetchEmployees() },[])

  const submit = async (e) => {
    e.preventDefault()
    const payload = {...form}
    await fetch(api + '/employees/', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)})
    setForm({emp_code:'', first_name:'', last_name:'', email:'', post:'GR-A', base_pay:''})
    fetchEmployees()
  }

  const generatePayrun = async () => {
    const year = new Date().getFullYear()
    const month = new Date().getMonth()+1
    const res = await fetch(`${api}/payrun/generate/${year}/${month}`, {method:'POST'})
    const data = await res.json()
    alert('Generated: ' + data.created)
  }

  const approvePayrun = async () => {
    const year = new Date().getFullYear()
    const month = new Date().getMonth()+1
    const res = await fetch(`${api}/payrun/approve/${year}/${month}`, {method:'POST'})
    const data = await res.json()
    alert('Approved: ' + data.approved)
  }

  return (
    <div style={{padding:20}}>
      <h1>Admin Portal - Payslip Generator</h1>

      <section style={{marginTop:20}}>
        <h3>Add Employee</h3>
        <form onSubmit={submit}>
          <input placeholder='code' value={form.emp_code} onChange={e=>setForm({...form, emp_code:e.target.value})} required/>
          <input placeholder='first name' value={form.first_name} onChange={e=>setForm({...form, first_name:e.target.value})} required/>
          <input placeholder='last name' value={form.last_name} onChange={e=>setForm({...form, last_name:e.target.value})} required/>
          <input placeholder='email' value={form.email} onChange={e=>setForm({...form, email:e.target.value})} required/>
          <select value={form.post} onChange={e=>setForm({...form, post:e.target.value})}>
            <option value='GR-A'>GR-A</option>
            <option value='GR-B'>GR-B</option>
          </select>
          <input placeholder='base pay' value={form.base_pay} onChange={e=>setForm({...form, base_pay:e.target.value})}/>
          <button type='submit'>Add</button>
        </form>
      </section>

      <section style={{marginTop:20}}>
        <button onClick={generatePayrun}>Generate Payrun (Draft)</button>
        <button onClick={approvePayrun} style={{marginLeft:8}}>Approve Payrun</button>
      </section>

      <h2 style={{marginTop:20}}>Employees</h2>
      <table border='1' cellPadding='8'>
        <thead><tr><th>ID</th><th>Code</th><th>Name</th><th>Email</th><th>Post</th></tr></thead>
        <tbody>
          {employees.map(e=>(
            <tr key={e.id}>
              <td>{e.id}</td>
              <td>{e.emp_code}</td>
              <td>{e.first_name} {e.last_name}</td>
              <td>{e.email}</td>
              <td>{e.post}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
