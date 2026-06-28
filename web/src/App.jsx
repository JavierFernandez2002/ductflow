import { useState } from "react";

const API = "http://localhost:8000/api/round-sizes";


function App() {
  const [flujo, setFlujo] = useState(0.5);
  const [perdida, setPerdida] = useState(0.8);
  const [resultado, setResultado] = useState(null)

  async function calcular() {
    try{
      const resp = await fetch(API, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({flow_rate_m3s: Number(flujo), target_pa_per_m: Number(perdida)})
      });
      const body = await resp.json();
      if(resp.ok){
        setResultado({status: "ok", data: body});
      } else {
        setResultado({status: "error", data: body.detail});
      }
    } catch(e){
      setResultado({status: "error", data: "No se pudo conectar con el servidor"});
    }
  }

  return (
  <div style={{fontFamily: "sans-serif", padding: 24, maxWidth: 420}}>
    <h1>DuctFlow</h1>
    <label>Caudal [m3/s]<input type="number" step="0.1" value={flujo}
    onChange={e => setFlujo(e.target.value)} /></label>
    <br />
    <label>Perdida objetivo [Pa/m]<input type="number" step="0.1" value={perdida}
    onChange={e => setPerdida(e.target.value)}/></label>
    <br/>
    <button onClick={calcular}>Dimensionar</button>

    {resultado?.status === "ok" &&(
      <div style={{marginTop: 16}}>
        <p>Diametro: <b>{resultado.data.diameter_m.toFixed(4)}</b></p>
        <p>Velocidad: <b>{resultado.data.velocity_ms.toFixed(2)}</b></p>
        <p>Reynolds: <b>{resultado.data.reynolds.toFixed(0)}</b></p>
      </div>
    )}
    {resultado?.status === "error" && (
      <p style={{ color: "crimson", marginTop: 16}}>⚠ {resultado.data}</p>
    )}
  </div>
  );
}

export default App
