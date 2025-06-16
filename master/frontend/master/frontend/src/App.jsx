import React, { useEffect, useState } from "react";

// 样式定义
const sidebarStyle = {
  width: "200px",
  background: "#f5f5f5",
  padding: "1rem",
  height: "100vh",
  boxSizing: "border-box",
  borderRight: "1px solid #e0e0e0"
};

const headerStyle = {
  background: "#1976d2",
  color: "#fff",
  padding: "1rem",
  fontSize: "1.5rem",
  letterSpacing: "2px",
  fontWeight: "bold",
  boxShadow: "0 2px 8px #1976d220"
};

const mainStyle = {
  flex: 1,
  padding: "2rem",
  background: "#fafbfc",
  minHeight: "calc(100vh - 64px)",
  overflowY: "auto"
};

const layoutStyle = {
  display: "flex",
  flexDirection: "column",
  height: "100vh"
};

const contentRowStyle = {
  display: "flex",
  flex: 1
};

const cardStyle = {
  background: "#fff",
  borderRadius: "12px",
  boxShadow: "0 2px 12px #1976d210",
  padding: "1.5rem",
  marginBottom: "2rem"
};

const sectionTitle = {
  fontSize: "1.2rem",
  fontWeight: "bold",
  color: "#1976d2",
  marginBottom: "1rem"
};

const weatherIcon = (icon) =>
  `https://openweathermap.org/img/wn/${icon}@2x.png`;

function formatDate(ts) {
  const d = new Date(ts * 1000);
  return `${d.getMonth() + 1}/${d.getDate()}`;
}

function formatHour(ts) {
  const d = new Date(ts * 1000);
  return `${d.getHours()}:00`;
}

function App() {
  // 默认北京经纬度
  const [lat] = useState(39.9042);
  const [lon] = useState(116.4074);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  useEffect(() => {
    setLoading(true);
    setErr(null);
    // TODO: 替换为你的 OpenWeather API KEY
    const API_KEY = "YOUR_API_KEY";
    fetch(
      `https://api.openweathermap.org/data/3.0/onecall?lat=${lat}&lon=${lon}&units=metric&lang=zh_cn&appid=${API_KEY}`
    )
      .then((res) => {
        if (!res.ok) throw new Error("网络错误");
        return res.json();
      })
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((e) => {
        setErr(e.message);
        setLoading(false);
      });
  }, [lat, lon]);

  return (
    <div style={layoutStyle}>
      {/* 顶部导航栏 */}
      <header style={headerStyle}>Master 天气管理页面</header>
      <div style={contentRowStyle}>
        {/* 侧边栏 */}
        <aside style={sidebarStyle}>
          <ul style={{ listStyle: "none", padding: 0 }}>
            <li style={{ margin: "1rem 0", color: "#1976d2", fontWeight: "bold" }}>仪表盘</li>
            <li style={{ margin: "1rem 0" }}>天气预报</li>
            <li style={{ margin: "1rem 0" }}>告警管理</li>
            <li style={{ margin: "1rem 0" }}>系统设置</li>
          </ul>
        </aside>
        {/* 主内容区 */}
        <main style={mainStyle}>
          {loading && <div style={cardStyle}>加载中...</div>}
          {err && <div style={{ ...cardStyle, color: "red" }}>加载失败：{err}</div>}
          {data && (
            <>
              {/* 当前天气 */}
              <section style={cardStyle}>
                <div style={sectionTitle}>当前天气（{data.timezone}）</div>
                <div style={{ display: "flex", alignItems: "center" }}>
                  <img
                    src={weatherIcon(data.current.weather[0].icon)}
                    alt={data.current.weather[0].description}
                    style={{ width: 80, height: 80, marginRight: 24 }}
                  />
                  <div>
                    <div style={{ fontSize: "2.5rem", fontWeight: "bold" }}>
                      {Math.round(data.current.temp)}°C
                    </div>
                    <div>{data.current.weather[0].description}</div>
                    <div>体感温度：{Math.round(data.current.feels_like)}°C</div>
                    <div>湿度：{data.current.humidity}%</div>
                    <div>风速：{data.current.wind_speed} m/s</div>
                  </div>
                </div>
              </section>

              {/* 未来12小时预报 */}
              <section style={cardStyle}>
                <div style={sectionTitle}>未来12小时预报</div>
                <div style={{ display: "flex", overflowX: "auto" }}>
                  {data.hourly.slice(0, 12).map((h, i) => (
                    <div
                      key={i}
                      style={{
                        minWidth: 80,
                        textAlign: "center",
                        marginRight: 16,
                        background: "#f0f4fa",
                        borderRadius: 8,
                        padding: "0.5rem"
                      }}
                    >
                      <div>{formatHour(h.dt)}</div>
                      <img
                        src={weatherIcon(h.weather[0].icon)}
                        alt={h.weather[0].description}
                        style={{ width: 40, height: 40 }}
                      />
                      <div style={{ fontWeight: "bold" }}>
                        {Math.round(h.temp)}°C
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              {/* 未来8天天气 */}
              <section style={cardStyle}>
                <div style={sectionTitle}>未来8天天气</div>
                <div style={{ display: "flex", flexWrap: "wrap" }}>
                  {data.daily.slice(0, 8).map((d, i) => (
                    <div
                      key={i}
                      style={{
                        flex: "1 0 120px",
                        minWidth: 120,
                        margin: "0 12px 12px 0",
                        background: "#f0f4fa",
                        borderRadius: 8,
                        padding: "0.5rem",
                        textAlign: "center"
                      }}
                    >
                      <div>{formatDate(d.dt)}</div>
                      <img
                        src={weatherIcon(d.weather[0].icon)}
                        alt={d.weather[0].description}
                        style={{ width: 40, height: 40 }}
                      />
                      <div style={{ fontWeight: "bold" }}>
                        {Math.round(d.temp.max)}° / {Math.round(d.temp.min)}°
                      </div>
                      <div style={{ fontSize: 12 }}>{d.weather[0].description}</div>
                    </div>
                  ))}
                </div>
              </section>

              {/* 天气警报 */}
              {data.alerts && data.alerts.length > 0 && (
                <section style={{ ...cardStyle, borderLeft: "6px solid #d32f2f" }}>
                  <div style={{ ...sectionTitle, color: "#d32f2f" }}>天气警报</div>
                  {data.alerts.map((a, i) => (
                    <div key={i} style={{ marginBottom: "1rem" }}>
                      <div style={{ fontWeight: "bold" }}>{a.event}</div>
                      <div style={{ fontSize: 12, color: "#888" }}>
                        {new Date(a.start * 1000).toLocaleString()} - {new Date(a.end * 1000).toLocaleString()}
                      </div>
                      <div>{a.description}</div>
                    </div>
                  ))}
                </section>
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;