import { useState, useMemo } from "react";
import {
  BarChart, Bar, LineChart, Line, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, RadarChart, Radar, PolarGrid,
  PolarAngleAxis, PolarRadiusAxis, PieChart, Pie, Cell
} from "recharts";

// ── Raw Data ──────────────────────────────────────────────────────────────────
const HOURLY_ALL = [
  {hour:6,label:"6 AM",revenue:21900.27,transactions:4594,avg_order:4.77},
  {hour:7,label:"7 AM",revenue:63526.47,transactions:13428,avg_order:4.73},
  {hour:8,label:"8 AM",revenue:82699.87,transactions:17654,avg_order:4.68},
  {hour:9,label:"9 AM",revenue:85169.53,transactions:17764,avg_order:4.79},
  {hour:10,label:"10 AM",revenue:88673.39,transactions:18545,avg_order:4.78},
  {hour:11,label:"11 AM",revenue:46319.14,transactions:9766,avg_order:4.74},
  {hour:12,label:"12 PM",revenue:40192.79,transactions:8708,avg_order:4.62},
  {hour:13,label:"1 PM",revenue:40367.45,transactions:8714,avg_order:4.63},
  {hour:14,label:"2 PM",revenue:41304.74,transactions:8933,avg_order:4.62},
  {hour:15,label:"3 PM",revenue:41733.1,transactions:8979,avg_order:4.65},
  {hour:16,label:"4 PM",revenue:41122.75,transactions:9093,avg_order:4.52},
  {hour:17,label:"5 PM",revenue:40134.31,transactions:8745,avg_order:4.59},
  {hour:18,label:"6 PM",revenue:34286.2,transactions:7498,avg_order:4.57},
  {hour:19,label:"7 PM",revenue:28446.68,transactions:6092,avg_order:4.67},
  {hour:20,label:"8 PM",revenue:2935.64,transactions:603,avg_order:4.87},
];

const HOURLY_LOC = [
  {store_location:"Astoria",hour:6,label:"6 AM",revenue:0,transactions:0},
  {store_location:"Astoria",hour:7,label:"7 AM",revenue:19028.8,transactions:4181},
  {store_location:"Astoria",hour:8,label:"8 AM",revenue:22805.9,transactions:4966},
  {store_location:"Astoria",hour:9,label:"9 AM",revenue:23183.57,transactions:5083},
  {store_location:"Astoria",hour:10,label:"10 AM",revenue:24426.12,transactions:5291},
  {store_location:"Astoria",hour:11,label:"11 AM",revenue:15498.13,transactions:3413},
  {store_location:"Astoria",hour:12,label:"12 PM",revenue:15681.2,transactions:3438},
  {store_location:"Astoria",hour:13,label:"1 PM",revenue:15947.87,transactions:3456},
  {store_location:"Astoria",hour:14,label:"2 PM",revenue:15175.27,transactions:3319},
  {store_location:"Astoria",hour:15,label:"3 PM",revenue:15651.95,transactions:3423},
  {store_location:"Astoria",hour:16,label:"4 PM",revenue:16110.85,transactions:3599},
  {store_location:"Astoria",hour:17,label:"5 PM",revenue:15839.3,transactions:3402},
  {store_location:"Astoria",hour:18,label:"6 PM",revenue:15951.3,transactions:3463},
  {store_location:"Astoria",hour:19,label:"7 PM",revenue:16943.65,transactions:3565},
  {store_location:"Astoria",hour:20,label:"8 PM",revenue:0,transactions:0},
  {store_location:"Hell's Kitchen",hour:6,label:"6 AM",revenue:7531.17,transactions:1676},
  {store_location:"Hell's Kitchen",hour:7,label:"7 AM",revenue:15961.05,transactions:3455},
  {store_location:"Hell's Kitchen",hour:8,label:"8 AM",revenue:31544.44,transactions:6909},
  {store_location:"Hell's Kitchen",hour:9,label:"9 AM",revenue:32874.29,transactions:6767},
  {store_location:"Hell's Kitchen",hour:10,label:"10 AM",revenue:33605.81,transactions:6957},
  {store_location:"Hell's Kitchen",hour:11,label:"11 AM",revenue:17926.54,transactions:3598},
  {store_location:"Hell's Kitchen",hour:12,label:"12 PM",revenue:11343.1,transactions:2442},
  {store_location:"Hell's Kitchen",hour:13,label:"1 PM",revenue:12070.1,transactions:2625},
  {store_location:"Hell's Kitchen",hour:14,label:"2 PM",revenue:12297.5,transactions:2754},
  {store_location:"Hell's Kitchen",hour:15,label:"3 PM",revenue:11311.25,transactions:2505},
  {store_location:"Hell's Kitchen",hour:16,label:"4 PM",revenue:11990.48,transactions:2691},
  {store_location:"Hell's Kitchen",hour:17,label:"5 PM",revenue:12789.5,transactions:2818},
  {store_location:"Hell's Kitchen",hour:18,label:"6 PM",revenue:11863.21,transactions:2608},
  {store_location:"Hell's Kitchen",hour:19,label:"7 PM",revenue:10766.36,transactions:2402},
  {store_location:"Hell's Kitchen",hour:20,label:"8 PM",revenue:2636.37,transactions:528},
  {store_location:"Lower Manhattan",hour:6,label:"6 AM",revenue:14369.1,transactions:2918},
  {store_location:"Lower Manhattan",hour:7,label:"7 AM",revenue:28536.62,transactions:5792},
  {store_location:"Lower Manhattan",hour:8,label:"8 AM",revenue:28349.53,transactions:5779},
  {store_location:"Lower Manhattan",hour:9,label:"9 AM",revenue:29111.67,transactions:5914},
  {store_location:"Lower Manhattan",hour:10,label:"10 AM",revenue:30641.46,transactions:6297},
  {store_location:"Lower Manhattan",hour:11,label:"11 AM",revenue:12894.47,transactions:2755},
  {store_location:"Lower Manhattan",hour:12,label:"12 PM",revenue:13168.49,transactions:2828},
  {store_location:"Lower Manhattan",hour:13,label:"1 PM",revenue:12349.48,transactions:2633},
  {store_location:"Lower Manhattan",hour:14,label:"2 PM",revenue:13831.97,transactions:2860},
  {store_location:"Lower Manhattan",hour:15,label:"3 PM",revenue:14769.9,transactions:3051},
  {store_location:"Lower Manhattan",hour:16,label:"4 PM",revenue:13021.42,transactions:2803},
  {store_location:"Lower Manhattan",hour:17,label:"5 PM",revenue:11505.51,transactions:2525},
  {store_location:"Lower Manhattan",hour:18,label:"6 PM",revenue:6471.69,transactions:1427},
  {store_location:"Lower Manhattan",hour:19,label:"7 PM",revenue:736.67,transactions:125},
  {store_location:"Lower Manhattan",hour:20,label:"8 PM",revenue:299.27,transactions:75},
];

const LOCATIONS = [
  {store_location:"Astoria",revenue:232243.91,transactions:50599,avg_order:4.59},
  {store_location:"Hell's Kitchen",revenue:236511.17,transactions:50735,avg_order:4.66},
  {store_location:"Lower Manhattan",revenue:230057.25,transactions:47782,avg_order:4.81},
];

const CATEGORIES = [
  {product_category:"Coffee",revenue:269952.45,transactions:58416},
  {product_category:"Tea",revenue:196405.95,transactions:45449},
  {product_category:"Bakery",revenue:82315.64,transactions:22796},
  {product_category:"Drinking Chocolate",revenue:72416.0,transactions:11468},
  {product_category:"Coffee beans",revenue:40085.25,transactions:1753},
  {product_category:"Branded",revenue:13607.0,transactions:747},
  {product_category:"Loose Tea",revenue:11213.6,transactions:1210},
  {product_category:"Flavours",revenue:8408.8,transactions:6790},
  {product_category:"Packaged Chocolate",revenue:4407.64,transactions:487},
];

const TOP_PRODUCTS = [
  {product_type:"Barista Espresso",revenue:91406.2,transactions:16403},
  {product_type:"Brewed Chai tea",revenue:77081.95,transactions:17183},
  {product_type:"Hot Chocolate",revenue:72416.0,transactions:11468},
  {product_type:"Gourmet Brewed Coffee",revenue:70034.6,transactions:16912},
  {product_type:"Brewed Black Tea",revenue:47932.0,transactions:11350},
  {product_type:"Brewed Herbal Tea",revenue:47539.5,transactions:11245},
  {product_type:"Premium Brewed Coffee",revenue:38781.15,transactions:8135},
  {product_type:"Organic Brewed Coffee",revenue:37746.5,transactions:8489},
  {product_type:"Scone",revenue:36866.12,transactions:10173},
  {product_type:"Drip Coffee",revenue:31984.0,transactions:8477},
];

const BUCKETS = [
  {time_bucket:"Morning",label:"Morning\n6–11 AM",revenue:388288.67,transactions:81751,pct:55.6},
  {time_bucket:"Afternoon",label:"Afternoon\n12–4 PM",revenue:204720.83,transactions:44427,pct:29.3},
  {time_bucket:"Evening",label:"Evening\n5–8 PM",revenue:105802.83,transactions:22938,pct:15.1},
];

const BUCKET_LOC = [
  {store_location:"Astoria",Morning:104942.52,Afternoon:78567.14,Evening:48734.25},
  {store_location:"Hell's Kitchen",Morning:139443.3,Afternoon:59012.43,Evening:38055.44},
  {store_location:"Lower Manhattan",Morning:143902.85,Afternoon:67141.26,Evening:19013.14},
];

const CAT_LOC = {
  "Astoria":    {Coffee:89744.3,Tea:67839.9,Bakery:26599.75,"Drinking Chocolate":26335.25,"Coffee beans":10219.2,Branded:5457,Flavours:1764.8,"Loose Tea":3194,"Packaged Chocolate":1089.71},
  "Hell's Kitchen": {Coffee:91222.65,Tea:64701.3,Bakery:27386.95,"Drinking Chocolate":23586.25,"Coffee beans":18635.1,Branded:1942,Flavours:2876.8,"Loose Tea":4461.35,"Packaged Chocolate":1698.77},
  "Lower Manhattan":{Coffee:88985.5,Tea:63864.75,Bakery:28328.94,"Drinking Chocolate":22494.5,"Coffee beans":11230.95,Branded:6208,Flavours:3767.2,"Loose Tea":3558.25,"Packaged Chocolate":1619.16},
};

// ── Constants ─────────────────────────────────────────────────────────────────
const AMBER = "#D97706";
const CREAM = "#FEF3C7";
const ESPRESSO = "#1C0A00";
const LATTE = "#C8956C";
const MOCHA = "#6B3A2A";
const STEAM = "#F5E6D3";

const LOC_COLORS = {
  "Astoria": "#D97706",
  "Hell's Kitchen": "#B45309",
  "Lower Manhattan": "#92400E",
};

const CAT_PALETTE = ["#D97706","#B45309","#92400E","#78350F","#C8956C","#6B3A2A","#A16207","#854D0E","#713F12"];

const fmt = (v) => v >= 1000 ? `$${(v/1000).toFixed(1)}K` : `$${v.toFixed(0)}`;
const fmtFull = (v) => `$${v.toLocaleString("en-US",{minimumFractionDigits:0,maximumFractionDigits:0})}`;

// ── Custom Tooltip ─────────────────────────────────────────────────────────────
const CoffeeTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{background:"#1C0A00",border:"1px solid #D97706",borderRadius:8,padding:"10px 14px",boxShadow:"0 8px 32px rgba(0,0,0,0.4)"}}>
      <p style={{color:"#FEF3C7",fontWeight:700,marginBottom:6,fontSize:13}}>{label}</p>
      {payload.map((p,i) => (
        <p key={i} style={{color:p.color||"#D97706",fontSize:12,margin:"2px 0"}}>
          {p.name}: <strong style={{color:"#FEF3C7"}}>{typeof p.value === "number" && p.name?.toLowerCase().includes("rev") ? fmtFull(p.value) : p.value?.toLocaleString()}</strong>
        </p>
      ))}
    </div>
  );
};

// ── KPI Card ──────────────────────────────────────────────────────────────────
const KpiCard = ({ label, value, sub, icon, highlight }) => (
  <div style={{
    background: highlight ? `linear-gradient(135deg, ${AMBER}, ${MOCHA})` : "rgba(28,10,0,0.6)",
    border: `1px solid ${highlight ? "transparent" : "rgba(217,119,6,0.3)"}`,
    borderRadius: 12,
    padding: "18px 20px",
    backdropFilter: "blur(8px)",
    flex: 1,
    minWidth: 140,
  }}>
    <div style={{fontSize:22,marginBottom:6}}>{icon}</div>
    <div style={{color: highlight ? "#FEF3C7" : "#D97706",fontSize:11,fontWeight:700,letterSpacing:2,textTransform:"uppercase",marginBottom:4}}>{label}</div>
    <div style={{color: highlight ? "#fff" : "#FEF3C7",fontSize:26,fontWeight:800,lineHeight:1}}>{value}</div>
    {sub && <div style={{color:highlight?"rgba(255,255,255,0.7)":"rgba(254,243,199,0.5)",fontSize:11,marginTop:4}}>{sub}</div>}
  </div>
);

// ── Section Title ─────────────────────────────────────────────────────────────
const SectionTitle = ({ children, sub }) => (
  <div style={{marginBottom:20}}>
    <h2 style={{color:"#FEF3C7",fontSize:18,fontWeight:800,letterSpacing:1,margin:0,fontFamily:"'Georgia',serif"}}>{children}</h2>
    {sub && <p style={{color:"rgba(200,149,108,0.7)",fontSize:12,margin:"4px 0 0",fontStyle:"italic"}}>{sub}</p>}
    <div style={{width:40,height:2,background:"linear-gradient(90deg, #D97706, transparent)",marginTop:8}}/>
  </div>
);

// ── Insight Box ───────────────────────────────────────────────────────────────
const Insight = ({ children, icon="☕" }) => (
  <div style={{
    background:"rgba(217,119,6,0.08)",
    border:"1px solid rgba(217,119,6,0.2)",
    borderLeft:"3px solid #D97706",
    borderRadius:8,
    padding:"10px 14px",
    marginTop:10,
    display:"flex",
    gap:10,
    alignItems:"flex-start",
  }}>
    <span style={{fontSize:16,flexShrink:0}}>{icon}</span>
    <p style={{color:"rgba(254,243,199,0.8)",fontSize:12,margin:0,lineHeight:1.6}}>{children}</p>
  </div>
);

// ── Main Dashboard ─────────────────────────────────────────────────────────────
export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("overview");
  const [selectedLoc, setSelectedLoc] = useState("All");
  const [metric, setMetric] = useState("revenue");

  const tabs = [
    {id:"overview",label:"📊 Overview"},
    {id:"hourly",label:"⏰ Hourly Demand"},
    {id:"locations",label:"📍 Locations"},
    {id:"products",label:"☕ Products"},
    {id:"insights",label:"💡 Insights"},
  ];

  const filteredHourly = useMemo(() => {
    if (selectedLoc === "All") return HOURLY_ALL;
    return HOURLY_LOC.filter(d => d.store_location === selectedLoc);
  }, [selectedLoc]);

  const pieData = CATEGORIES.map((c,i) => ({
    name: c.product_category,
    value: c.revenue,
    color: CAT_PALETTE[i],
  }));

  const radarData = HOURLY_ALL.filter(h => h.hour >= 7 && h.hour <= 19).map(h => ({
    time: h.label,
    Astoria: HOURLY_LOC.find(d=>d.store_location==="Astoria"&&d.hour===h.hour)?.transactions||0,
    "Hell's Kitchen": HOURLY_LOC.find(d=>d.store_location==="Hell's Kitchen"&&d.hour===h.hour)?.transactions||0,
    "Lower Manhattan": HOURLY_LOC.find(d=>d.store_location==="Lower Manhattan"&&d.hour===h.hour)?.transactions||0,
  }));

  return (
    <div style={{
      minHeight:"100vh",
      background:`radial-gradient(ellipse at 20% 20%, rgba(107,58,42,0.4) 0%, transparent 60%),
                  radial-gradient(ellipse at 80% 80%, rgba(217,119,6,0.15) 0%, transparent 60%),
                  linear-gradient(160deg, #0D0500 0%, #1C0A00 40%, #0A0300 100%)`,
      fontFamily:"'Trebuchet MS', sans-serif",
      color:"#FEF3C7",
      padding:"0 0 40px",
    }}>

      {/* Header */}
      <div style={{
        background:"rgba(28,10,0,0.8)",
        borderBottom:"1px solid rgba(217,119,6,0.3)",
        backdropFilter:"blur(16px)",
        padding:"20px 32px",
        display:"flex",
        alignItems:"center",
        justifyContent:"space-between",
        position:"sticky",
        top:0,
        zIndex:100,
      }}>
        <div>
          <div style={{display:"flex",alignItems:"center",gap:12}}>
            <span style={{fontSize:28}}>☕</span>
            <div>
              <h1 style={{margin:0,fontSize:22,fontWeight:900,letterSpacing:2,fontFamily:"'Georgia',serif",
                background:"linear-gradient(90deg, #FEF3C7, #D97706)",
                WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent"}}>
                AFFICIONADO COFFEE ROASTERS
              </h1>
              <p style={{margin:0,fontSize:11,color:"rgba(200,149,108,0.7)",letterSpacing:3,textTransform:"uppercase"}}>
                Temporal Sales Analytics Dashboard · 2025
              </p>
            </div>
          </div>
        </div>
        <div style={{display:"flex",gap:8,alignItems:"center"}}>
          {["All","Astoria","Hell's Kitchen","Lower Manhattan"].map(loc => (
            <button key={loc} onClick={()=>setSelectedLoc(loc)} style={{
              padding:"6px 12px",
              borderRadius:20,
              border:`1px solid ${selectedLoc===loc?"#D97706":"rgba(217,119,6,0.2)"}`,
              background:selectedLoc===loc?"rgba(217,119,6,0.2)":"transparent",
              color:selectedLoc===loc?"#FEF3C7":"rgba(200,149,108,0.6)",
              fontSize:11,
              fontWeight:600,
              cursor:"pointer",
              letterSpacing:0.5,
            }}>{loc}</button>
          ))}
        </div>
      </div>

      {/* Tabs */}
      <div style={{
        display:"flex",gap:4,padding:"16px 32px 0",
        borderBottom:"1px solid rgba(217,119,6,0.15)",
      }}>
        {tabs.map(t => (
          <button key={t.id} onClick={()=>setActiveTab(t.id)} style={{
            padding:"10px 18px",
            background:activeTab===t.id?"rgba(217,119,6,0.15)":"transparent",
            border:"none",
            borderBottom:activeTab===t.id?`2px solid #D97706`:"2px solid transparent",
            color:activeTab===t.id?"#FEF3C7":"rgba(200,149,108,0.5)",
            fontSize:12,
            fontWeight:700,
            cursor:"pointer",
            letterSpacing:0.5,
          }}>{t.label}</button>
        ))}
      </div>

      <div style={{padding:"28px 32px"}}>

        {/* ── OVERVIEW TAB ── */}
        {activeTab === "overview" && (
          <div>
            {/* KPIs */}
            <div style={{display:"flex",gap:14,marginBottom:32,flexWrap:"wrap"}}>
              <KpiCard icon="💰" label="Total Revenue" value="$698.8K" sub="2025 YTD · All Locations" highlight />
              <KpiCard icon="🧾" label="Transactions" value="149,116" sub="Avg 4.69 per order" />
              <KpiCard icon="📦" label="Units Sold" value="214,470" sub="Avg 1.44 qty/transaction" />
              <KpiCard icon="⏰" label="Peak Hour" value="10 AM" sub="18,545 transactions" />
              <KpiCard icon="🏆" label="Top Location" value="Hell's Kitchen" sub="$236.5K revenue" />
              <KpiCard icon="☕" label="Top Product" value="Barista Espresso" sub="$91.4K revenue" />
            </div>

            {/* Time Bucket Summary */}
            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:24,marginBottom:28}}>
              <div style={{background:"rgba(28,10,0,0.6)",border:"1px solid rgba(217,119,6,0.2)",borderRadius:12,padding:20}}>
                <SectionTitle sub="Revenue distribution by time period">Time Period Breakdown</SectionTitle>
                {BUCKETS.map((b,i) => (
                  <div key={b.time_bucket} style={{marginBottom:14}}>
                    <div style={{display:"flex",justifyContent:"space-between",marginBottom:5}}>
                      <span style={{color:"#C8956C",fontSize:13,fontWeight:600}}>{b.time_bucket}</span>
                      <span style={{color:"#FEF3C7",fontSize:13,fontWeight:700}}>{fmtFull(b.revenue)} <span style={{color:"#D97706",fontSize:11}}>({b.pct}%)</span></span>
                    </div>
                    <div style={{background:"rgba(255,255,255,0.05)",borderRadius:4,height:8}}>
                      <div style={{width:`${b.pct}%`,height:8,borderRadius:4,background:`linear-gradient(90deg, ${CAT_PALETTE[i]}, ${CAT_PALETTE[i+1]||AMBER})`}}/>
                    </div>
                    <div style={{color:"rgba(200,149,108,0.5)",fontSize:11,marginTop:3}}>{b.transactions.toLocaleString()} transactions</div>
                  </div>
                ))}
                <Insight>Morning (6–11 AM) drives 55.6% of total revenue — the undisputed king of the trading day.</Insight>
              </div>

              <div style={{background:"rgba(28,10,0,0.6)",border:"1px solid rgba(217,119,6,0.2)",borderRadius:12,padding:20}}>
                <SectionTitle sub="Revenue split across all three cafés">Store Performance</SectionTitle>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={LOCATIONS} margin={{top:5,right:10,left:0,bottom:5}}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(217,119,6,0.1)"/>
                    <XAxis dataKey="store_location" tick={{fill:"#C8956C",fontSize:10}} tickFormatter={v=>v.split(" ")[0]}/>
                    <YAxis tickFormatter={fmt} tick={{fill:"#C8956C",fontSize:10}}/>
                    <Tooltip content={<CoffeeTooltip/>}/>
                    <Bar dataKey="revenue" name="Revenue" radius={[4,4,0,0]}>
                      {LOCATIONS.map((l,i)=><Cell key={i} fill={Object.values(LOC_COLORS)[i]}/>)}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
                <div style={{display:"flex",gap:10,marginTop:8}}>
                  {LOCATIONS.map(l=>(
                    <div key={l.store_location} style={{flex:1,textAlign:"center",background:"rgba(217,119,6,0.05)",borderRadius:6,padding:"8px 4px"}}>
                      <div style={{color:"#D97706",fontSize:10,fontWeight:700}}>{l.store_location.split(" ")[0]}</div>
                      <div style={{color:"#FEF3C7",fontSize:14,fontWeight:800}}>${(l.avg_order).toFixed(2)}</div>
                      <div style={{color:"rgba(200,149,108,0.5)",fontSize:10}}>avg order</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Category Pie + Time bucket by loc */}
            <div style={{display:"grid",gridTemplateColumns:"1fr 1.4fr",gap:24}}>
              <div style={{background:"rgba(28,10,0,0.6)",border:"1px solid rgba(217,119,6,0.2)",borderRadius:12,padding:20}}>
                <SectionTitle sub="Revenue share by category">Product Mix</SectionTitle>
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart>
                    <Pie data={pieData} cx="50%" cy="50%" innerRadius={55} outerRadius={85}
                         dataKey="value" nameKey="name" paddingAngle={2}>
                      {pieData.map((e,i)=><Cell key={i} fill={e.color}/>)}
                    </Pie>
                    <Tooltip formatter={(v)=>[fmtFull(v),"Revenue"]} contentStyle={{background:"#1C0A00",border:"1px solid #D97706",borderRadius:8}}/>
                  </PieChart>
                </ResponsiveContainer>
                <div style={{display:"flex",flexWrap:"wrap",gap:6,marginTop:8}}>
                  {pieData.slice(0,6).map((d,i)=>(
                    <div key={i} style={{display:"flex",alignItems:"center",gap:4,fontSize:10}}>
                      <div style={{width:8,height:8,borderRadius:2,background:d.color,flexShrink:0}}/>
                      <span style={{color:"rgba(200,149,108,0.7)"}}>{d.name}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div style={{background:"rgba(28,10,0,0.6)",border:"1px solid rgba(217,119,6,0.2)",borderRadius:12,padding:20}}>
                <SectionTitle sub="How each location's revenue is distributed across the day">Time Bucket by Location</SectionTitle>
                <ResponsiveContainer width="100%" height={220}>
                  <BarChart data={BUCKET_LOC} margin={{top:5,right:10,left:0,bottom:5}}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(217,119,6,0.1)"/>
                    <XAxis dataKey="store_location" tick={{fill:"#C8956C",fontSize:10}} tickFormatter={v=>v.split(" ")[0]}/>
                    <YAxis tickFormatter={fmt} tick={{fill:"#C8956C",fontSize:10}}/>
                    <Tooltip content={<CoffeeTooltip/>}/>
                    <Legend wrapperStyle={{fontSize:11,color:"#C8956C"}}/>
                    <Bar dataKey="Morning" fill="#D97706" radius={[2,2,0,0]}/>
                    <Bar dataKey="Afternoon" fill="#B45309" radius={[2,2,0,0]}/>
                    <Bar dataKey="Evening" fill="#92400E" radius={[2,2,0,0]}/>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {/* ── HOURLY DEMAND TAB ── */}
        {activeTab === "hourly" && (
          <div>
            <div style={{display:"flex",gap:8,marginBottom:20}}>
              {["revenue","transactions"].map(m=>(
                <button key={m} onClick={()=>setMetric(m)} style={{
                  padding:"8px 16px",borderRadius:20,fontSize:12,fontWeight:700,cursor:"pointer",
                  border:`1px solid ${metric===m?"#D97706":"rgba(217,119,6,0.3)"}`,
                  background:metric===m?"rgba(217,119,6,0.2)":"transparent",
                  color:metric===m?"#FEF3C7":"rgba(200,149,108,0.5)",
                  letterSpacing:0.5,
                }}>{metric===m?"▶ ":""}{m.charAt(0).toUpperCase()+m.slice(1)}</button>
              ))}
            </div>

            {/* Main hourly area chart */}
            <div style={{background:"rgba(28,10,0,0.6)",border:"1px solid rgba(217,119,6,0.2)",borderRadius:12,padding:20,marginBottom:24}}>
              <SectionTitle sub={`${metric==="revenue"?"Revenue ($)":"Transaction count"} by hour · ${selectedLoc}`}>
                Hourly {metric === "revenue" ? "Revenue" : "Transaction Volume"} Curve
              </SectionTitle>
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={filteredHourly} margin={{top:10,right:20,left:10,bottom:5}}>
                  <defs>
                    <linearGradient id="revGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#D97706" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="#D97706" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(217,119,6,0.08)"/>
                  <XAxis dataKey="label" tick={{fill:"#C8956C",fontSize:11}}/>
                  <YAxis tickFormatter={metric==="revenue"?fmt:v=>v.toLocaleString()} tick={{fill:"#C8956C",fontSize:11}}/>
                  <Tooltip content={<CoffeeTooltip/>}/>
                  <Area type="monotone" dataKey={metric} name={metric==="revenue"?"Revenue":"Transactions"}
                    stroke="#D97706" strokeWidth={2.5} fill="url(#revGrad)" dot={{fill:"#D97706",r:4}}/>
                </AreaChart>
              </ResponsiveContainer>
              <Insight icon="⏰">
                Peak activity occurs at <strong>10 AM</strong> with 18,545 transactions and $88,673 in revenue.
                There is a sharp drop-off after 11 AM (–47%) followed by a stable afternoon plateau,
                then a gradual evening decline. Operations after 7 PM are minimal.
              </Insight>
            </div>

            {/* Hourly comparison by location */}
            <div style={{background:"rgba(28,10,0,0.6)",border:"1px solid rgba(217,119,6,0.2)",borderRadius:12,padding:20,marginBottom:24}}>
              <SectionTitle sub="Transaction volumes compared across all three locations hour by hour">Location Comparison by Hour</SectionTitle>
              <ResponsiveContainer width="100%" height={260}>
                <LineChart margin={{top:10,right:20,left:10,bottom:5}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(217,119,6,0.08)"/>
                  <XAxis dataKey="label" type="category" allowDuplicatedCategory={false}
                    tick={{fill:"#C8956C",fontSize:11}}/>
                  <YAxis tickFormatter={v=>v.toLocaleString()} tick={{fill:"#C8956C",fontSize:11}}/>
                  <Tooltip content={<CoffeeTooltip/>}/>
                  <Legend wrapperStyle={{fontSize:11,color:"#C8956C"}}/>
                  {Object.entries(LOC_COLORS).map(([loc,color])=>(
                    <Line key={loc} data={HOURLY_LOC.filter(d=>d.store_location===loc)}
                      type="monotone" dataKey={metric} name={loc}
                      stroke={color} strokeWidth={2} dot={{r:3}} connectNulls/>
                  ))}
                </LineChart>
              </ResponsiveContainer>
              <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:10,marginTop:12}}>
                <Insight icon="🏙️">
                  <strong>Lower Manhattan</strong> peaks earliest (6 AM pre-commute wave) and drops sharply after 6 PM — a classic business-district pattern.
                </Insight>
                <Insight icon="🚇">
                  <strong>Hell's Kitchen</strong> shows the strongest morning surge (8–10 AM) driven by commuter and transit traffic. Clear bimodal pattern.
                </Insight>
                <Insight icon="🏘️">
                  <strong>Astoria</strong> is the most temporally uniform — a residential area with steady demand throughout the day and active evenings.
                </Insight>
              </div>
            </div>

            {/* Heatmap grid */}
            <div style={{background:"rgba(28,10,0,0.6)",border:"1px solid rgba(217,119,6,0.2)",borderRadius:12,padding:20}}>
              <SectionTitle sub="Transaction intensity — darker = more activity">Transaction Heatmap by Location × Hour</SectionTitle>
              {Object.entries(LOC_COLORS).map(([loc, color]) => {
                const locData = HOURLY_LOC.filter(d=>d.store_location===loc);
                const max = Math.max(...locData.map(d=>d.transactions));
                return (
                  <div key={loc} style={{marginBottom:16}}>
                    <div style={{color:"#C8956C",fontSize:12,fontWeight:700,marginBottom:6}}>{loc}</div>
                    <div style={{display:"flex",gap:3}}>
                      {HOURLY_ALL.map(h => {
                        const d = locData.find(x=>x.hour===h.hour);
                        const intensity = d ? d.transactions/max : 0;
                        return (
                          <div key={h.hour} title={`${h.label}: ${d?.transactions?.toLocaleString()||0} txns`}
                            style={{
                              flex:1, height:36, borderRadius:4,
                              background:`rgba(217,119,6,${0.05+intensity*0.9})`,
                              border:`1px solid rgba(217,119,6,${0.1+intensity*0.3})`,
                              display:"flex",alignItems:"center",justifyContent:"center",
                              fontSize:9,color:`rgba(254,243,199,${0.3+intensity*0.7})`,
                              fontWeight:700,
                            }}>
                            {h.label.replace(" ","").replace("AM","a").replace("PM","p")}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
              <div style={{display:"flex",alignItems:"center",gap:8,marginTop:10}}>
                <span style={{color:"rgba(200,149,108,0.5)",fontSize:11}}>Low</span>
                <div style={{display:"flex",gap:2}}>
                  {[0.1,0.3,0.5,0.7,0.9].map(o=><div key={o} style={{width:20,height:10,borderRadius:2,background:`rgba(217,119,6,${o})`}}/>)}
                </div>
                <span style={{color:"rgba(200,149,108,0.5)",fontSize:11}}>High</span>
              </div>
            </div>
          </div>
        )}

        {/* ── LOCATIONS TAB ── */}
        {activeTab === "locations" && (
          <div>
            <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:16,marginBottom:24}}>
              {LOCATIONS.map(l=>(
                <div key={l.store_location} style={{
                  background:"rgba(28,10,0,0.6)",
                  border:`1px solid ${LOC_COLORS[l.store_location]}44`,
                  borderTop:`3px solid ${LOC_COLORS[l.store_location]}`,
                  borderRadius:12,padding:20,
                }}>
                  <div style={{color:LOC_COLORS[l.store_location],fontSize:13,fontWeight:800,marginBottom:12,letterSpacing:1}}>
                    📍 {l.store_location.toUpperCase()}
                  </div>
                  {[
                    ["Total Revenue",fmtFull(l.revenue)],
                    ["Transactions",l.transactions.toLocaleString()],
                    ["Avg Order Value",`$${l.avg_order.toFixed(2)}`],
                    ["Revenue Share",`${(l.revenue/698812.33*100).toFixed(1)}%`],
                  ].map(([k,v])=>(
                    <div key={k} style={{display:"flex",justifyContent:"space-between",borderBottom:"1px solid rgba(217,119,6,0.1)",padding:"8px 0"}}>
                      <span style={{color:"rgba(200,149,108,0.6)",fontSize:12}}>{k}</span>
                      <span style={{color:"#FEF3C7",fontSize:12,fontWeight:700}}>{v}</span>
                    </div>
                  ))}
                </div>
              ))}
            </div>

            {/* Category by location stacked bar */}
            <div style={{background:"rgba(28,10,0,0.6)",border:"1px solid rgba(217,119,6,0.2)",borderRadius:12,padding:20,marginBottom:24}}>
              <SectionTitle sub="Category revenue breakdown per store">Product Category Mix by Location</SectionTitle>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={Object.entries(CAT_LOC).map(([loc,cats])=>({name:loc.split(" ")[0],...cats}))}
                  margin={{top:10,right:20,left:10,bottom:5}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(217,119,6,0.08)"/>
                  <XAxis dataKey="name" tick={{fill:"#C8956C",fontSize:11}}/>
                  <YAxis tickFormatter={fmt} tick={{fill:"#C8956C",fontSize:11}}/>
                  <Tooltip content={<CoffeeTooltip/>}/>
                  <Legend wrapperStyle={{fontSize:10,color:"#C8956C"}}/>
                  {["Coffee","Tea","Bakery","Drinking Chocolate","Coffee beans"].map((cat,i)=>(
                    <Bar key={cat} dataKey={cat} stackId="a" fill={CAT_PALETTE[i]} radius={i===4?[4,4,0,0]:[0,0,0,0]}/>
                  ))}
                </BarChart>
              </ResponsiveContainer>
              <Insight icon="📊">
                Coffee and Tea dominate across all three locations (55–60% combined). Hell's Kitchen leads in Coffee Bean sales ($18.6K) vs Astoria ($10.2K), suggesting a more barista-savvy clientele.
              </Insight>
            </div>

            {/* Radar comparison */}
            <div style={{background:"rgba(28,10,0,0.6)",border:"1px solid rgba(217,119,6,0.2)",borderRadius:12,padding:20}}>
              <SectionTitle sub="Hourly transaction profile — how each store's day is shaped">Temporal Profile Radar by Location</SectionTitle>
              <ResponsiveContainer width="100%" height={320}>
                <RadarChart data={radarData.filter((_,i)=>i%2===0)}>
                  <PolarGrid stroke="rgba(217,119,6,0.2)"/>
                  <PolarAngleAxis dataKey="time" tick={{fill:"#C8956C",fontSize:10}}/>
                  <PolarRadiusAxis tick={{fill:"rgba(200,149,108,0.4)",fontSize:9}}/>
                  <Tooltip content={<CoffeeTooltip/>}/>
                  <Legend wrapperStyle={{fontSize:11,color:"#C8956C"}}/>
                  {Object.entries(LOC_COLORS).map(([loc,color])=>(
                    <Radar key={loc} name={loc} dataKey={loc} stroke={color} fill={color} fillOpacity={0.12} strokeWidth={2}/>
                  ))}
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* ── PRODUCTS TAB ── */}
        {activeTab === "products" && (
          <div>
            <div style={{display:"grid",gridTemplateColumns:"1.2fr 1fr",gap:24,marginBottom:24}}>
              <div style={{background:"rgba(28,10,0,0.6)",border:"1px solid rgba(217,119,6,0.2)",borderRadius:12,padding:20}}>
                <SectionTitle sub="Top 10 product types by revenue">Revenue by Product Type</SectionTitle>
                <ResponsiveContainer width="100%" height={320}>
                  <BarChart data={TOP_PRODUCTS} layout="vertical" margin={{top:5,right:20,left:100,bottom:5}}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(217,119,6,0.08)" horizontal={false}/>
                    <XAxis type="number" tickFormatter={fmt} tick={{fill:"#C8956C",fontSize:10}}/>
                    <YAxis type="category" dataKey="product_type" tick={{fill:"#C8956C",fontSize:11}} width={110}/>
                    <Tooltip content={<CoffeeTooltip/>}/>
                    <Bar dataKey="revenue" name="Revenue" radius={[0,4,4,0]}>
                      {TOP_PRODUCTS.map((_,i)=><Cell key={i} fill={`rgba(217,119,6,${1-i*0.07})`}/>)}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div style={{display:"flex",flexDirection:"column",gap:16}}>
                <div style={{background:"rgba(28,10,0,0.6)",border:"1px solid rgba(217,119,6,0.2)",borderRadius:12,padding:20}}>
                  <SectionTitle sub="Revenue by product category">Category Breakdown</SectionTitle>
                  <ResponsiveContainer width="100%" height={180}>
                    <BarChart data={CATEGORIES.slice(0,6)} margin={{top:5,right:10,left:0,bottom:30}}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(217,119,6,0.08)"/>
                      <XAxis dataKey="product_category" tick={{fill:"#C8956C",fontSize:9}} angle={-30} textAnchor="end"/>
                      <YAxis tickFormatter={fmt} tick={{fill:"#C8956C",fontSize:9}}/>
                      <Tooltip content={<CoffeeTooltip/>}/>
                      <Bar dataKey="revenue" name="Revenue" radius={[3,3,0,0]}>
                        {CATEGORIES.slice(0,6).map((_,i)=><Cell key={i} fill={CAT_PALETTE[i]}/>)}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div style={{background:"rgba(28,10,0,0.6)",border:"1px solid rgba(217,119,6,0.2)",borderRadius:12,padding:20}}>
                  <SectionTitle sub="Key product performance metrics">Product Highlights</SectionTitle>
                  {TOP_PRODUCTS.slice(0,4).map((p,i)=>(
                    <div key={p.product_type} style={{display:"flex",justifyContent:"space-between",
                      borderBottom:"1px solid rgba(217,119,6,0.1)",padding:"8px 0"}}>
                      <div>
                        <div style={{color:"#FEF3C7",fontSize:12,fontWeight:600}}>#{i+1} {p.product_type}</div>
                        <div style={{color:"rgba(200,149,108,0.5)",fontSize:10}}>{p.transactions.toLocaleString()} transactions</div>
                      </div>
                      <div style={{color:"#D97706",fontSize:14,fontWeight:800}}>{fmtFull(p.revenue)}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <Insight icon="🏆">
              <strong>Barista Espresso</strong> is the single highest-revenue product at $91,406 but <strong>Brewed Chai Tea</strong> leads in transaction volume (17,183), suggesting Espresso commands a higher average price per order.
              Coffee (as a category) represents 38.6% of all revenue — the clear revenue anchor.
            </Insight>
          </div>
        )}

        {/* ── INSIGHTS TAB ── */}
        {activeTab === "insights" && (
          <div>
            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:20}}>

              {[
                {
                  icon:"⏰", title:"Peak Hour Intelligence",
                  findings:[
                    "10 AM is the single busiest hour with 18,545 transactions — 3x the volume of off-peak hours",
                    "The 8–10 AM window (morning rush) generates 36.7% of daily revenue in just 3 hours",
                    "Transaction volume drops 47% between 11 AM and noon — a sharp post-rush cliff",
                    "Afternoon (12–4 PM) plateau is stable at ~8,900 transactions/hour with minimal variance",
                    "After 7 PM, volumes collapse — operations after 8 PM represent <0.5% of daily revenue",
                  ],
                  rec:"Concentrate maximum staffing 8–11 AM. Skeleton crew sufficient after 7 PM.",
                  color:"#D97706"
                },
                {
                  icon:"📍", title:"Location Behavioral Profiles",
                  findings:[
                    "Lower Manhattan opens earliest at 6 AM with 2,918 transactions — pre-commute workers",
                    "Hell's Kitchen has the sharpest morning peak and drops most steeply post-11 AM",
                    "Astoria is the most uniform throughout the day — evenings at 7 PM still have 3,565 transactions",
                    "Lower Manhattan has the highest avg order value ($4.81) — business clientele spend more",
                    "Astoria evening trade exceeds Hell's Kitchen, Lower Manhattan — residential dynamic",
                  ],
                  rec:"Tailor staff schedules by location character, not a one-size-fits-all template.",
                  color:"#B45309"
                },
                {
                  icon:"☕", title:"Product & Revenue Strategy",
                  findings:[
                    "Coffee (38.6%) and Tea (28.1%) together represent 66.7% of all revenue",
                    "Barista Espresso at $91,406 revenue is the single most valuable product",
                    "Hot Chocolate ($72,416) outperforms Bakery on revenue despite fewer transaction types",
                    "Coffee Beans ($40K, 1,753 txns) have the highest avg order value — premium segment",
                    "Flavours (6,790 txns) with only $8,408 revenue suggest a low unit-price add-on category",
                  ],
                  rec:"Upsell strategies and bundling should anchor around Espresso + Bakery morning combos.",
                  color:"#92400E"
                },
                {
                  icon:"📋", title:"Operational Recommendations",
                  findings:[
                    "Morning rush (8–11 AM): deploy maximum staff across all 3 locations — non-negotiable",
                    "Astoria: extend evening operational hours — there is proven demand post-5 PM",
                    "Lower Manhattan: consider reduced operating hours past 7 PM (minimal revenue)",
                    "Hell's Kitchen: prioritize espresso-machine staffing — commuter speed is critical",
                    "Afternoon lull (12–4 PM): ideal window for staff breaks, restocking, training",
                  ],
                  rec:"A shift model of 6 AM–3 PM and 11 AM–8 PM with overlapping peak coverage is recommended.",
                  color:"#78350F"
                },
              ].map(card=>(
                <div key={card.title} style={{background:"rgba(28,10,0,0.6)",border:`1px solid ${card.color}33`,
                  borderTop:`3px solid ${card.color}`,borderRadius:12,padding:20}}>
                  <div style={{color:card.color,fontSize:16,marginBottom:8}}>{card.icon}</div>
                  <h3 style={{color:"#FEF3C7",fontSize:15,fontWeight:800,margin:"0 0 14px",fontFamily:"'Georgia',serif"}}>{card.title}</h3>
                  <ul style={{margin:0,paddingLeft:16}}>
                    {card.findings.map((f,i)=>(
                      <li key={i} style={{color:"rgba(200,149,108,0.8)",fontSize:12,marginBottom:8,lineHeight:1.5}}>{f}</li>
                    ))}
                  </ul>
                  <div style={{background:`${card.color}15`,border:`1px solid ${card.color}33`,borderRadius:6,
                    padding:"10px 12px",marginTop:14,display:"flex",gap:8,alignItems:"flex-start"}}>
                    <span style={{color:card.color,fontSize:14,flexShrink:0}}>→</span>
                    <p style={{color:"#FEF3C7",fontSize:12,margin:0,fontWeight:600}}>{card.rec}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* Executive Summary Box */}
            <div style={{
              marginTop:24,
              background:"linear-gradient(135deg, rgba(107,58,42,0.4), rgba(28,10,0,0.8))",
              border:"1px solid rgba(217,119,6,0.4)",
              borderRadius:12,padding:24,
            }}>
              <h3 style={{color:"#FEF3C7",fontSize:16,fontWeight:800,margin:"0 0 14px",fontFamily:"'Georgia',serif"}}>
                📄 Executive Summary
              </h3>
              <p style={{color:"rgba(200,149,108,0.85)",fontSize:13,lineHeight:1.8,margin:0}}>
                Afficionado Coffee Roasters processed <strong style={{color:"#FEF3C7"}}>149,116 transactions</strong> generating{" "}
                <strong style={{color:"#D97706"}}>$698,812 in revenue</strong> across three New York City locations in 2025.
                The data reveals that <strong style={{color:"#FEF3C7"}}>55.6% of all revenue occurs in a 6-hour morning window (6–11 AM)</strong>,
                with the absolute peak at 10 AM. Each location exhibits a distinct behavioral archetype: Lower Manhattan serves
                early-rising business professionals, Hell's Kitchen captures high-volume commuter traffic, and Astoria maintains
                the most balanced daily curve with significant evening demand. Coffee (38.6%) and Tea (28.1%) anchor the product mix.
                These findings enable data-driven decisions on staffing schedules, operating hours, and menu promotion strategies
                — replacing intuition-led management with quantitative evidence.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={{textAlign:"center",color:"rgba(200,149,108,0.3)",fontSize:11,marginTop:20,letterSpacing:1}}>
        AFFICIONADO COFFEE ROASTERS · TEMPORAL SALES ANALYTICS · 2025 · 149,116 TRANSACTIONS ANALYSED
      </div>
    </div>
  );
}
