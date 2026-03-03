import React, { useEffect, useState } from "react";

function App() {
  const [plans, setPlans] = useState([]);
  const [title, setTitle] = useState("");
  const [employeeId, setEmployeeId] = useState("");
  const [status, setStatus] = useState("");

  const API = "http://localhost:8000/api/plans";

  const fetchPlans = async () => {
    const res = await fetch(API);
    const data = await res.json();
    setPlans(data);
  };

  const createPlan = async () => {
    await fetch(API, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        employee_id: Number(employeeId),
        title,
        status
      })
    });

    setTitle("");
    setEmployeeId("");
    setStatus("");
    fetchPlans();
  };

  const deletePlan = async (id) => {
    await fetch(`${API}/${id}`, {
      method: "DELETE"
    });
    fetchPlans();
  };

  useEffect(() => {
    fetchPlans();
  }, []);

  return (
    <div style={{ padding: 30 }}>
      <h1>Планы развития</h1>

      <div>
        <input
          placeholder="ID сотрудника"
          value={employeeId}
          onChange={(e) => setEmployeeId(e.target.value)}
        />
        <input
          placeholder="Название плана"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          placeholder="Статус"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        />
        <button onClick={createPlan}>Создать</button>
      </div>

      <hr />

      <ul>
        {plans.map((plan) => (
          <li key={plan.id}>
            {plan.title} | сотрудник: {plan.employee_id} | статус: {plan.status}
            <button onClick={() => deletePlan(plan.id)}>Удалить</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;